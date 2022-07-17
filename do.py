#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--interact', '-i', action='store_true')
parser.add_argument('--command', '-c')
parser.add_argument('--test', '-t', action='store_true')
parser.add_argument('--package', '-p', action='store_true')
args = parser.parse_args()

DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(DIR)

if args.interact:
    subprocess.run(['python3', '-i', '-c', 'import dansplotcore; from dansplotcore import plot'])

if args.command:
    subprocess.run(['python3', '-c', 'import dansplotcore; from dansplotcore import plot; '+args.command])

if args.test:
    subprocess.run(['python3', 'test.py'])

if args.package:
    os.chdir('package')
    shutil.rmtree('dansplotcore', ignore_errors=True)
    shutil.rmtree('dansplotcore.egg-info', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.copytree(os.path.join('..', 'dansplotcore'), 'dansplotcore')
    subprocess.run('python3 setup.py sdist'.split())
    subprocess.run('twine upload dist/*'.split())
    os.chdir('..')
