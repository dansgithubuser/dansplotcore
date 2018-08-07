import argparse
import os
import shutil
import subprocess

parser=argparse.ArgumentParser()
parser.add_argument('--build', '-b', action='store_true')
parser.add_argument('--package', '-p', action='store_true')
args=parser.parse_args()

LOC=os.path.dirname(os.path.realpath(__file__))
os.chdir(LOC)

def invoke(invocation):
	subprocess.check_call(invocation.split())

def copy_into(path):
	shutil.copyfile(path, os.path.join('dansplotcore', os.path.basename(path)))

if args.build:
	try: os.mkdir('built')
	except: pass
	os.chdir('built')
	invoke('cmake -DCMAKE_BUILD_TYPE=Release ../danssfml/wrapper')
	invoke('cmake --build . --config Release')
	os.chdir('..')

if args.package:
	os.chdir('package')
	shutil.copyfile(os.path.join('..', 'dansplotcore.py'), os.path.join('dansplotcore', '__init__.py'))
	invoke('python3 setup.py sdist')
	invoke('twine upload dist/*')
	os.chdir('..')
