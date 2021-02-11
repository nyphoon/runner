import time
import threading
from subprocess import Popen, PIPE, STDOUT


def run_command(cmd, success_cb=None, error_cb=None):
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    output = p.stdout.read().decode()
    
    if p.wait() == 0:
        if success_cb is not None:
            success_cb(cmd, p.pid, output)
    else:
        if error_cb is not None:
            error_cb(cmd, p.pid, output)


class CommandRunner:
    def __init__(self, run_max=None, success_cb=None, error_cb=None):
        self._run_max= run_max or 5
        self._waiting_queue = []
        self._running_threads = {}
        self._success_cb = success_cb
        self._error_cb = error_cb
    
    def get_waitings(self):
        return self._waiting_queue

    def get_runnings(self):
        return [r for r in self._running_threads]

    def submit(self, cmd):
        self._waiting_queue.append(cmd)

    def _run(self):
        while True:
            tt = []  # terminated threads
            for r, t in self._running_threads.items():
                if not t.is_alive():
                    t.join()
                    tt.append(r)
            for t in tt:
                del self._running_threads[t]

            while len(self._running_threads) < self._run_max and \
                    len(self._waiting_queue) > 0:
                cmd = self._waiting_queue.pop(0)
                t = threading.Thread(target=run_command,
                                     args=(cmd,
                                        self._success_cb,
                                        self._error_cb),
                                     daemon=True)
                self._running_threads[cmd] = t
                t.start()
            time.sleep(1)

    def run(self):
        threading.Thread(target=self._run, daemon=True).start()
