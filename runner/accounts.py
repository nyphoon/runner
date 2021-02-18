import json
import hashlib
import uuid


def _encode_password(password):
    salt = str(uuid.uuid4())[:8]
    m = hashlib.sha256()
    m.update(password.encode())
    m.update(salt.encode())
    return salt + m.hexdigest()


def _verify_password(encoded_password, password):
    salt = encoded_password[:8]
    m = hashlib.sha256()
    m.update(password.encode())
    m.update(salt.encode())
    return m.hexdigest() == encoded_password[8:]


class Accounts:
    def __init__(self, json_path=None):
        self._accounts = {}
        if json_path is not None:
            self.load(json_path)

    def load(self, json_path):
        with open(json_path, 'r') as f:
            self._accounts = json.load(f)['accounts']

    def auth(self, name, password):
        return name in self._accounts and \
               _verify_password(self._accounts[name]['password'], password)

    def new(self, name, password, config=None):
        if name in self._accounts:
            raise ValueError(f'account existed {name}')
        self._accounts[name] = {'password': _encode_password(password),
                                'config': config or {}}

    def save(self, json_path):
        with open(json_path, 'w') as f:
            json.dump({'accounts': self._accounts}, f, indent=2)

    def get_info(self, name):
        if name not in self._accounts:
            raise ValueError(f'account not existed {name}')
        return {'name': name,
                **self._accounts[name]['config']}


if __name__ == '__main__':
    def create_account():
        a = Accounts('accounts.json')  # append new account
        # a = Accounts() # new accounts json
        name = input('name:')
        password = input('password:')
        config_json = input('config json:')
        config = json.loads(config_json)
        a.new(name, password, config)
        a.save('accounts.json')

    while True:
        create_account()
