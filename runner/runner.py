import time
import threading
import uuid
from subprocess import Popen, PIPE, STDOUT


def run_command(task_id, cmd, arg_dict, user_info,
                start_cb=None, success_cb=None, fail_cb=None):
    if start_cb is not None:
        start_cb(task_id, cmd, arg_dict, user_info)

    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True, cwd=user_info['wd'])
    output = p.stdout.read().decode()

    if p.wait() == 0:
        if success_cb is not None:
            success_cb(task_id, cmd, arg_dict, user_info, p.pid, output)
    else:
        if fail_cb is not None:
            fail_cb(task_id, cmd, arg_dict, user_info, p.pid, output)


class CommandRunner:
    def __init__(self, run_max=None):
        self._run_max= run_max or 5
        self._waiting_queue = []
        self._running_threads = {}

    def get_waitings(self):
        return self._waiting_queue

    def get_runnings(self):
        return list(self._running_threads.keys())

    def submit(self, cmd: dict):
        self._waiting_queue.append(cmd)

    def _run(self):
        while True:
            tt = []  # terminated threads
            for r, t in self._running_threads.items():
                if not t.is_alive():
                    t.join()
                    tt.append(r)
            for r in tt:
                del self._running_threads[r]

            while len(self._running_threads) < self._run_max and \
                    len(self._waiting_queue) > 0:
                cmd = self._waiting_queue.pop(0)
                task_id = uuid.uuid4()
                t = threading.Thread(target=run_command,
                                     args=(
                                         task_id,
                                         cmd['cmd'],
                                         cmd['arg'],
                                         cmd['user_info'],
                                         cmd['start_cb'],
                                         cmd['success_cb'],
                                         cmd['fail_cb']
                                         ),
                                     daemon=True)
                self._running_threads[task_id] = t
                t.start()
            time.sleep(1)

    def run(self):
        threading.Thread(target=self._run, daemon=True).start()
