from functools import wraps
from flask import Flask, request, jsonify, app, g
from runner import CommandRunner
from accounts import Accounts


app = Flask(__name__)

accounts = Accounts('accounts.json')

def auth(func):
    @wraps(func)
    def auth_decorator(*args, **kwargs):
        name = request.headers.get('X-Runner-User')
        password = request.headers.get('X-Runner-Password')
        if name is None or password is None:
            return 'Unauthorized', 401
        if accounts.auth(name, password) is False:
            return 'Forbidden', 403
        g.user_info = accounts.get_info(name)
        return func(*args, **kwargs)
    return auth_decorator


def success_cb(cmd, pid, output):
    print(f'---- success {pid} {cmd} ----')
    print(output)


def error_cb(cmd, pid, output):
    print(f'---- error {pid} {cmd} ----')
    print(output)


runner = CommandRunner(5, success_cb, error_cb)
runner.run()


@app.route('/waiting', methods=['GET'])
@auth
def list_waiting():
    return jsonify({'waiting_tasks': runner.get_waitings()})


@app.route('/running', methods=['GET'])
@auth
def list_running():
    return jsonify({'running_tasks': runner.get_runnings()})


@app.route('/', methods=['PUT'])
@auth
def submit_task():
    cmd = request.json.get('cmd')
    runner.submit(cmd)
    return jsonify({'a':1})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
