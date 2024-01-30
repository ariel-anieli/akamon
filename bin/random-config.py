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

def snmp():
    version   = secrets.choice(['1', '2', '3'])
    sec_level = secrets.choice(['authPriv','authNoPriv','noAuthNoPriv'])
    sec_set   = lambda level: {
        'authNoPriv'   : {
            'authentication-protocol' : secrets.choice(['MD5', 'SHA']),
            'authentication-password' : pswd(4),
        },
        'authPriv'     : {
            'authentication-protocol' : secrets.choice(['MD5', 'SHA']),
            'authentication-password' : pswd(4),
            'privacy-protocol'        : secrets.choice(['AES', 'DES']),
            'privacy-passphrase'      : pswd(4)
        },
        'noAuthNoPriv' : {}
    }[level]

    default = {
        'version'                 : version,
        'community'               : '',
        'username'                : '',
        'security-level'          : '',
        'authentication-protocol' : '',
        'authentication-password' : '',
        'privacy-protocol'        : '',
        'privacy-passphrase'      : ''
    }
    setup   = {
        '1' : {
            'community' : pswd(4),
        },
        '2' : {
            'community' : pswd(4),
        },
        '3' : {
            'security-level' : sec_level,
            'username'       : pswd(4),
        } | sec_set(sec_level)
    }[version]

    return default | setup

if __name__ == "__main__":
    pipe(
        range(int(sys.argv[1])),
        lambda devs: functools.reduce(add_dev_to_config, devs, config_template()),
        json.dumps,
        print
    )
