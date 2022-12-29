#!/usr/bin/env python3
import secrets
import string
import re

import hashlib
import base64
import random

FILES = {
    "bin/grafana/datasources/influxdb.yml": {"token": "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"},
    "bin/mosquitto/pwfile": {"home-assistant": ""},
    "bin/grafana.env": {"GF_DATABASE_PASSWORD": "POSTGRES_GRAFANA_PASSWORD"},
    "bin/influxdb.env": ["DOCKER_INFLUXDB_INIT_PASSWORD", "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"],
    "bin/postgres.env": ["POSTGRES_PASSWORD", "POSTGRES_GRAFANA_PASSWORD"],
    "bin/zwavejs.env": ["SESSION_SECRET"],
    "configs/home-assistant/secrets.yaml": {"influxdb_token": "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN", "recorder_db": "POSTGRES_PASSWORD"}
}

PASSWORDS = {}


def _generate_password():
    letters = string.ascii_letters
    digits = string.digits
    special_chars = '!#$%&()*+,-./;<>?[]^_{|}'  # string.punctuation
    alphabet = letters + digits + special_chars
    pwd_length = 24 + secrets.randbelow(8)
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))

    return (pwd)


def _generate_mosquitto_password(pwd):
    # https://stackoverflow.com/questions/63265141/mosquitto-password-generation-in-python
    chars = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    salt = bytes([random.choice(chars) for i in range(16)])
    saltB64 = base64.b64decode(salt)

    passwd = bytes(pwd, encoding='utf-8')

    m = hashlib.sha512()
    m.update(passwd)
    m.update(saltB64)
    dg = m.digest()

    return ('$6$%s$%s' % (repr(salt)[2:-1], repr(base64.b64encode(dg))[2:-1]))


def create_passwords():
    for f in FILES:
        if type(FILES[f]) is list:
            for l in FILES[f]:
                PASSWORDS[l] = _generate_password()


def replace_passwords():
    for f in FILES:
        if type(FILES[f]) is list:
            for key in FILES[f]:
                if key in PASSWORDS:
                    value = PASSWORDS[key]
                else:
                    value = _generate_password()
                _replace_password(f, key, value)
        if type(FILES[f]) is dict:
            for key in FILES[f]:
                if FILES[f][key] in PASSWORDS:
                    if key == 'recorder_db':
                        value = f'postgresql://home-assistant:{PASSWORDS[FILES[f][key]]}@postgres/home-assistant'
                    else:
                        value = PASSWORDS[FILES[f][key]]
                else:
                    value = _generate_password()
                _replace_password(f, key, value)


def _replace_password(target, key, value):
    print(f'Replacing password in {target} for {key} with {value}')

    if target[-3:] == 'yml' or target[-4:] == 'yaml':
        _replace_in_file(target, key, value, ending='yaml')
    elif target[-6:] == 'pwfile':
        _replace_in_file(target, key, value, ending='pwfile')
    else:
        _replace_in_file(target, key, value)


def _replace_in_file(target, key, value, ending='env'):
    if ending == 'pwfile':
        value = _generate_mosquitto_password(value)

    with open(target, 'r+') as f:
        file = f.read()

        if ending == 'yaml':
            file = re.sub(r"{}:.*".format(key),
                          r"{}: '{}'".format(key, value), file)
        elif ending == 'pwfile':
            file = re.sub(r"{}:.*".format(key),
                          r"{}:{}".format(key, value), file)
        else:
            file = re.sub(r"{}=.*".format(key),
                          r"{}={}".format(key, value), file)

        f.seek(0)
        f.write(file)
        f.truncate()


def main():
    print('Setting up passwords...')
    create_passwords()
    replace_passwords()


if __name__ == '__main__':
    main()
