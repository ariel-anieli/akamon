import datetime
import functools
import json
import os
import sys
import uuid

def community(snmp):
    return '-c {}'.format(snmp['community'])

def security(snmp):
    auth = lambda: '-a {} -A {}'.format(
        snmp['authentication-protocol'],
        snmp['authentication-password']
    )

    priv = lambda: '-x {} -X {}'.format(
        snmp['privacy-protocol'],
        snmp['privacy-passphrase']
    )

    match snmp['security-level']:
        case 'authPriv':
            return ' '.join([auth(), priv()])
        case 'authNoPriv':
            return auth()
        case 'noAuthNoPriv':
            return ''

def time():
    return datetime.datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z')

def command(snmp):
    match snmp['version']:
        case '1':
            return ' '.join(['-v1', community(snmp)])
        case '2':
            return ' '.join(['-v2c', community(snmp)])
        case '3':
            level = snmp['security-level']
            user  = snmp['username']
            return ' '.join(['-l {} -u {}'.format(level, user), security(snmp)])

def test_device(cmd, device):
    snmp  = ' '.join([
        'snmpwalk',
        command(device['snmp']),
        device['ip'],
        'system'
    ])
    shell = "sh -c '{}'".format(snmp)
    test  = ' '.join([cmd, shell])

    print(json.dumps({
        'time'    : time(),
        'message' : 'test',
        'id'      : str(uuid.uuid4()),
        'device'  : device['name'],
        'command' : {
            'input'  : snmp,
            'output' : os.popen(test).read()
            
        }
    }))

    return cmd

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as system:
        config  = json.loads(system.read())

    functools.reduce(
        test_device,
        config['device'],
        'sudo docker exec -it {}'.format(config['container']['id']),
    )
