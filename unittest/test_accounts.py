import os
import json
import pytest
from accounts import Accounts

@pytest.fixture()
def json_path():
    _path = 'unittest_accounts.json'
    if os.path.exists(_path):
        os.remove(_path)
    with open(_path, 'w') as f:
        json.dump({'accounts':{}}, f, indent=2)
    return _path

def test_basic(json_path):
    a = Accounts(json_path)
    a.new('user1', '1234')
    a.save('unittest_accounts.json')

    b = Accounts(json_path)
    assert b.auth('user1', '123') is False
    assert b.auth('user2', '1234') is False
    assert b.auth('user1', '1234') is True
    