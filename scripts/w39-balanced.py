"""Diagnostic process launcher on task-owned distinct upstream ports."""
import argparse
import signal
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('--version', choices=['baseline', 'candidate'], required=True)
parser.add_argument('--workers', type=int, choices=[8, 16], default=8)
args = parser.parse_args()
children = []
stopped = False

def stop(*_):
    global stopped
    stopped = True

signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
try:
    for port in range(58160, 58160 + args.workers):
        children.append(subprocess.Popen([sys.executable, 'scripts/w39-serve.py',
            '--version', args.version, '--port', str(port), '--workers', '1']))
    while not stopped and all(child.poll() is None for child in children):
        time.sleep(.1)
finally:
    for child in children:
        if child.poll() is None:
            child.terminate()
    deadline = time.monotonic() + 4
    for child in children:
        try:
            child.wait(timeout=max(.01, deadline-time.monotonic()))
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()
