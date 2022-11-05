import functools
import json
import secrets
import string
import sys

chrs = string.ascii_letters + string.digits
pswd = lambda size: ''.join(secrets.choice(chrs) for i in range(size))

global_ = lambda: {
    "name"   : pswd(8),
    "id"     : pswd(8),
    "device" : []
}
device  = lambda: {
    'name'     : pswd(8),
    'ip'       : '.'.join(str(secrets.randbelow(256)) for i in range(4)),
    'username' : 'admin',
    'password' : '',
    'type'     : secrets.choice(['FMG', 'FGT', 'FAZ']),
    'snmp'     : snmp()
}

def pipe(args, *funcs):
    return functools.reduce(lambda arg, fn: fn(arg), funcs, args)

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

def device_template(template, index):
    devices = template['device']
    devices.append(device())
    return template | {'device' : devices}

if __name__ == "__main__":
    pipe(
        functools.reduce(device_template, range(int(sys.argv[1])), global_()),
        json.dumps,
        print
    )
