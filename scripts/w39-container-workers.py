"""Task-only distinct-port workers inside the single API container."""
import os
import signal
import subprocess
import sys
import time

stopped = False
def stop(*_):
    global stopped
    stopped = True
signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
children = []
try:
    for port in range(8000, 8008):
        children.append(subprocess.Popen([sys.executable, '-m', 'uvicorn',
            'w39_instrumented:create_app' if os.environ.get('W39_INSTRUMENT') == '1' else 'custometry_api.main:create_app',
            '--factory', '--host', '0.0.0.0', '--port', str(port), '--workers', '1',
            '--timeout-graceful-shutdown', '2', '--log-level', 'warning', '--no-access-log']))
    while not stopped and all(child.poll() is None for child in children):
        time.sleep(.1)
finally:
    for child in children:
        if child.poll() is None:
            child.terminate()
    for child in children:
        try:
            child.wait(timeout=2)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()
