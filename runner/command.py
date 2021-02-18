import json
from logging_result import LoggingResult


def _get_logging_result(arg_dict, user_info):
    name = '{}.{}'.format(user_info['name'], arg_dict['cmd'])
    result_path = '{}/{}.log'.format(user_info['wd'], name)

    logging_result = LoggingResult()
    logger = logging_result.get_logger(name)
    return logger or logging_result.create_logger(name, result_path)


def logging_start_cb(tid, cmd, arg_dict, user_info):
    result = _get_logging_result(arg_dict, user_info)
    result.info('%s start:\n cmd=%s\n arg=%s\n user_info=%s',
                str(tid), cmd, json.dumps(arg_dict), json.dumps(user_info))


def logging_success_cb(tid, cmd, arg_dict, user_info, pid, output):
    result = _get_logging_result(arg_dict, user_info)
    result.info('%s success: \n%s', str(tid), output)


def logging_fail_cb(tid, cmd, arg_dict, user_info, pid, output):
    result = _get_logging_result(arg_dict, user_info)
    result.info('%s fail: \n%s', str(tid), output)


def demo_start_cb(tid, cmd, arg_dict, user_info):
    print(f'---- {tid} start {cmd} ----')


def demo_success_cb(tid, cmd, arg_dict, user_info, pid, output):
    print(f'---- {tid} success {pid} {cmd} ----')
    print(output)
    print(f'---- {tid} success ----')


def demo_fail_cb(tid, cmd, arg_dict, user_info, pid, output):
    print(f'---- {tid} fail {pid} {cmd} ----')
    print(output)
    print(f'---- {tid} fail ----')


def make_demo_cmd_dict(cmd: str):
    return {
        'cmd': cmd,
        'start_cb': demo_start_cb,
        'success_cb': demo_success_cb,
        'fail_cb': demo_fail_cb
    }


def get_cmd_dict(cmd, arg_dict):
    cmd_dict = _CMD_DICT.get(cmd)
    if cmd_dict is None:
        return None
    try:
        cmd = cmd_dict['cmd'].format(**arg_dict)
    except KeyError:  # bad arg
        return None
    return {
        'cmd': cmd,
        'start_cb': cmd_dict['start_cb'],
        'success_cb': cmd_dict['success_cb'],
        'fail_cb': cmd_dict['fail_cb']
    }


_CMD_DICT = {
    'download': {
        'cmd': 'curl -o {save_as} {url}',
        'start_cb': logging_start_cb,
        'success_cb': logging_success_cb,
        'fail_cb': logging_fail_cb
    }
}
