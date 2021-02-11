from runner import run_command, CommandRunner


def test_demo():
    def success_cb(cmd, pid, output):
        print(f'---- success {pid} {cmd} ----')
        print(output)

    def error_cb(cmd, pid, output):
        print(f'---- error {pid} {cmd} ----')
        print(output)

    cmd = 'python job_sleep.py a 1'
    run_command(cmd, success_cb, error_cb)

    r = CommandRunner(2, success_cb, error_cb)
    r.submit('ls -l')
    r.submit('python job_except.py a 3')
    r.run()
    r.submit('python job_sleep.py b 5')
    r.submit('python job_sleep.py b 5')

    time.sleep(10)
