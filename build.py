import os
import subprocess

def invoke(invocation):
	subprocess.check_call(invocation.split())

try: os.mkdir('built')
except: pass
os.chdir('built')
invoke('cmake -DCMAKE_BUILD_TYPE=Release ../danssfml/wrapper')
invoke('cmake --build . --config Release')
