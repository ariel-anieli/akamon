import datetime
import functools
import json
import os
import sys
import uuid

time = datetime.datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z')
one  = lambda snmp: '-v1 -c {}'.format(snmp['community'])
two  = lambda snmp: '-v2c -c {}'.format(snmp['community'])

def three(snmp):
    authNoPriv   = '-l authNoPriv -u {} -a {} -A {}'.format(
        snmp['username'],
        snmp['authentication-protocol'],
        snmp['authentication-password']
    )
    authPriv     = '-l authPriv -u {} -a {} -A {} -x {} -X {}'.format(
        snmp['username'],
        snmp['authentication-protocol'],
        snmp['authentication-password'],
        snmp['privacy-protocol'],
        snmp['privacy-passphrase']
    )
    noAuthNoPriv = '-v3 -l noAuthNoPriv -u {}'.format(snmp['username'])

    return {
        'authNoPriv'   : authNoPriv,
        'authPriv'     : authPriv,
        'noAuthNoPriv' : noAuthNoPriv
    }[snmp['security-level']]

def command(snmp):
    version = snmp['version']
    if version=='1':
        return one(snmp)
    elif version=='2':
        return two(snmp)
    else:
        return three(snmp)

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
        'time'    : time,
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
