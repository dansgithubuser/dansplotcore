#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--build', '-b', action='store_true')
parser.add_argument('--interact', '-i', action='store_true')
parser.add_argument('--command', '-c')
parser.add_argument('--test', '-t', action='store_true')
parser.add_argument('--package', '-p', action='store_true')
args = parser.parse_args()

DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(DIR)

def invoke(invocation):
    subprocess.check_call(invocation.split())

def copy_into(path):
    shutil.copyfile(path, os.path.join('dansplotcore', os.path.basename(path)))

def build():
    try: os.mkdir('built')
    except: pass
    os.chdir('built')
    invoke('cmake -DCMAKE_BUILD_TYPE=Release ../danssfml/wrapper')
    invoke('cmake --build . --config Release')
    os.chdir('..')

if args.build:
    build()

if args.interact:
    subprocess.check_call(['python', '-i', '-c', 'import dansplotcore; from dansplotcore import plot'])

if args.command:
    subprocess.check_call(['python', '-c', 'import dansplotcore; from dansplotcore import plot; '+args.command])

if args.test:
    invoke('python test.py')

if args.package:
    build()
    os.chdir('package')
    shutil.rmtree('dansplotcore', ignore_errors=True)
    shutil.rmtree('dansplotcore.egg-info', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    os.mkdir('dansplotcore')
    shutil.copyfile(os.path.join('..', 'dansplotcore.py'), os.path.join('dansplotcore', '__init__.py'))
    invoke('python3 setup.py sdist')
    invoke('twine upload dist/*')
    os.chdir('..')
