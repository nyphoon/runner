from functools import wraps
from flask import Flask, request, jsonify, app, g
from .runner import CommandRunner
from .accounts import Accounts
from .command import make_demo_cmd_dict, get_cmd_dict


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

runner = CommandRunner()
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
    if cmd is None:
        cmd = request.json.get('cmd_code')
        if cmd is not None and g.user_config.get('class') == 'super':
            cmd_dict = make_demo_cmd_dict(cmd)
            cmd_dict['user_info'] = g.user_info
            cmd_dict['arg'] = request.json
            runner.submit(cmd_dict)
            return jsonify({'result': 'super'})
        return 'Bad Request', 400

    cmd_dict = get_cmd_dict(cmd, request.json)
    if cmd_dict is None:
        return 'Bad Request', 400
    cmd_dict['user_info'] = g.user_info
    cmd_dict['arg'] = request.json
    runner.submit(cmd_dict)
    return jsonify({'result': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
