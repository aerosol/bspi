#!/usr/bin/env python3

import json
import os
import re
import subprocess
import sys
import argparse
import configparser

script_dir = os.path.dirname(os.path.realpath(__file__))
default_config_loc = f'{script_dir}/bspi.ini'

parser = argparse.ArgumentParser(description='bspi - rename bspwm desktops with icons based on the applications \
    currently running under that desktop')
parser.add_argument('-c', '--config', default=f'{default_config_loc}', help='absolute or relative path to the bspi \
    configuration file')
args = parser.parse_args()


class Icon:
    def __init__(self, client_class=None):
        self.client_class = client_class
        self.ICONS = self._config()

    def __str__(self):
        return self.ICONS.get(self.client_class.lower(), self.ICONS.get('_other'))

    def _config(self):
        config = configparser.ConfigParser()
        if os.path.isfile(args.config):
            config.read_file(open(args.config))
            return config['Icons']

        else:
            exit(f"No file was found at the specified path for the configuration file\npath: {args.config}")


class Bspwm:
    @staticmethod
    def world():
        result = subprocess.run(['bspc', 'wm', '-d'], stdout=subprocess.PIPE)
        return json.loads(result.stdout)

    @staticmethod
    def rename_desktop(id, name):
        subprocess.run(['bspc', 'desktop', str(id), '--rename', name],
                stdout=subprocess.PIPE)

class X11:
    @staticmethod
    def xprop_class(id):
        result = subprocess.run(['xprop', '-id', str(id), '-notype', 'WM_CLASS'],
                stdout=subprocess.PIPE)
        return re.sub(r'[",]', '', result.stdout.split()[2].decode('utf8'))

class Node:
    def __init__(self, data):
        self._data = data
        if data['client']:
            self.client = data['client']
            if self.client['className']:
                self.client_class = self.client['className']
            else:
                # Sometimes bspwm does not recognize client's WM class. 
                # Happens with Chromium here. This extra subprocess call should work then.
                self.client_class = X11.xprop_class(self._data['id'])
        else:
            self.client = None
            self.client_class = None

    @property
    def id(self):
        return self._data['id']

    @property
    def name(self):
        return self._data['name']

    @property
    def is_sticky(self):
        return self._data['sticky']

    @property
    def deduced_name(self):
        if self.client_classes:
            return ' '.join([str(Icon(client_class)) for client_class in
                    self.client_classes])
        else:
            return ""

    @property
    def client_classes(self):
        cs = [child.client_class for child in self.all_children if not child.is_sticky]

        if self.client_class and not self.is_sticky:
            cs.append(self.client_class)

        return list(filter(None, cs))

    @property
    def first_child(self):
        if self._data.get('firstChild'):
            return Node(self._data['firstChild'])
        return None

    @property
    def second_child(self):
        if self._data.get('secondChild'):
            return Node(self._data['secondChild'])
        return None

    @property
    def all_children(self):
        first_child = self.first_child
        if first_child:
            yield first_child
            for child in first_child.all_children:
                yield child

        second_child = self.second_child
        if second_child:
            yield second_child
            for child in second_child.all_children:
                yield child

    def __str__(self):
        return "<Node(%s %s)>" % (self.id, self.client_classes)

if __name__ == "__main__":
    world = Bspwm.world()

    for monitor in world['monitors']:
        for desktop in monitor['desktops']:
            if desktop['root']:
                node = Node(desktop['root'])
                if desktop['name'] != node.deduced_name:
                    print("Renaming desktop: %s" % node)
                    Bspwm.rename_desktop(desktop['id'], node.deduced_name)

            else:
                Bspwm.rename_desktop(desktop['id'], Icon()._config().get('_other'))
