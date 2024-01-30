import functools
import json
import secrets
import string
import sys

def config_template():
    return {
        "name"   : pswd(8),
        "id"     : pswd(8),
        "device" : []
    }

def device():
    return {
        'name'     : pswd(8),
        'ip'       : '.'.join(str(secrets.randbelow(256)) for i in range(4)),
        'username' : 'admin',
        'password' : '',
        'type'     : secrets.choice(['FMG', 'FGT', 'FAZ']),
        'snmp'     : snmp()
    }

def add_dev_to_config(template, index):
    devices = template['device']
    devices.append(device())
    return template | {'device' : devices}

def pipe(args, *funcs):
    return functools.reduce(lambda arg, func: func(arg), funcs, args)

def pswd(size):
    charset = string.ascii_letters + string.digits
    return ''.join(secrets.choice(charset) for i in range(size))

def set_security(level):
    auth = lambda: {
        'authentication-protocol' : secrets.choice(['MD5', 'SHA']),
        'authentication-password' : pswd(4),
    }

    priv = lambda: {
        'privacy-protocol'        : secrets.choice(['AES', 'DES']),
        'privacy-passphrase'      : pswd(4)
    }

    match level:
        case 'authPriv':
            return auth() | priv()
        case 'authNoPriv':
            return auth()
        case 'noAuthNoPriv':
            return {}

def snmp_defaults():
    return {
        'community'               : '',
        'username'                : '',
        'security-level'          : '',
        'authentication-protocol' : '',
        'authentication-password' : '',
        'privacy-protocol'        : '',
        'privacy-passphrase'      : ''
    }

def snmp_params(version):
    community = lambda: {
        'community' : pswd(4)
    }

    security = lambda level: {
        'security-level' : level,
        'username'       : pswd(4)
    } | set_security(level)

    match version:
        case '1' | '2':
            params = community()
        case '3':
            level  = secrets.choice(['authPriv','authNoPriv','noAuthNoPriv'])
            params = security(level)

    return {'version' : version} | params

def snmp():
    version = secrets.choice(['1', '2', '3'])
    return snmp_defaults() | snmp_params(version)

if __name__ == "__main__":
    pipe(
        range(int(sys.argv[1])),
        lambda devs: functools.reduce(add_dev_to_config, devs, config_template()),
        json.dumps,
        print
    )
