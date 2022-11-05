import functools
import json
import sys

def is_ipv4(addr):
    return len(addr.split('.'))==4 \
        and all([int(byte)<256 and int(byte)>=0 for byte in addr.split('.')])

contract = {
'ip' : {'term'     : lambda addr: is_ipv4(addr),
        'error'    : 'Invalid IPv4 address',
        'severity' : 'major'},
'name' : {'term'     : lambda name: isinstance(name, str) and len(name)>0,
          'error'    : 'Device name should be non-empty string',
          'severity' : 'minor'},
'version'   : {'term'     : lambda version: version in ['1', '2', '3'],
               'error'    : 'SNMP version must be 1, 2, or 3',
               'severity' : 'major'},
'community' : {'term'     : lambda comm: isinstance(comm, str) and len(comm)>0,
               'error'    : 'Community name should be non-empty string',
               'severity' : 'minor'},
'username' : {'term'     : lambda user: isinstance(user, str) and len(user)>0,
              'error'    : 'Username should be non-empty string',
              'severity' : 'minor'},
'authentication-protocol' : {'term'     : lambda auth: auth in ['MD5', 'SHA'],
                             'error'    : 'Authentication protocol is either MD5 or SHA',
                             'severity' : 'minor'},
'authentication-password' : {'term'     : lambda name: isinstance(name, str) and len(name)>0,
                             'error'    : 'Authentication password should be non-empty string',
                             'severity' : 'minor'},
'privacy-protocol' : {'term'     : lambda auth: auth in ['AES', 'DES'],
                      'error'    : 'Privacy protocol is either AES or DES',
                      'severity' : 'minor'},
'privacy-passphrase' : {'term'     : lambda name: isinstance(name, str) and len(name)>0,
                      'error'    : 'Privacy passphrase should be non-empty string',
                      'severity' : 'minor'},
'security-level' : {'term'     : lambda sec: sec in ['authPriv','authNoPriv','noAuthNoPriv'],
                    'error'    : 'Security level is either authPriv, authNoPriv, noAuthNoPriv',
                    'severity' : 'major'}
}

def check(agreement):
    contract, contractor = agreement
    return {
        'valid?'   : contract['term'](contractor),
        'error'    : contract['error'],
        'severity' : contract['severity']
    }

def check_device(reports, device):
    report     = {'name' : device['name'],
                  'ip'   : device['ip']}
    contracts   = [
        contract['version'],
        contract['ip'],
        contract['name']
    ]
    contractors = [
        device['snmp']['version'],
        device['ip'],
        device['name']
    ]

    if device['snmp']['version'] in ['1', '2']:
        contracts.append(contract['community'])
        contractors.append(device['snmp']['community'])
    elif device['snmp']['version']=='3':
        contracts.append(contract['security-level'])
        contractors.append(device['snmp']['security-level'])
        if device['snmp']['security-level']=='noAuthNoPriv':
            contracts.append(contract['username'])
            contractors.append(device['snmp']['username'])
        elif device['snmp']['security-level']=='authNoPriv':
            contracts.append(contract['username'])
            contracts.append(contract['authentication-protocol'])
            contracts.append(contract['authentication-password'])

            contractors.append(device['snmp']['username'])
            contractors.append(device['snmp']['authentication-protocol'])
            contractors.append(device['snmp']['authentication-password'])
        elif device['snmp']['security-level']=='authPriv':
            contracts.append(contract['username'])
            contracts.append(contract['authentication-protocol'])
            contracts.append(contract['authentication-password'])
            contracts.append(contract['privacy-protocol'])
            contracts.append(contract['privacy-passphrase'])

            contractors.append(device['snmp']['username'])
            contractors.append(device['snmp']['authentication-protocol'])
            contractors.append(device['snmp']['authentication-password'])
            contractors.append(device['snmp']['privacy-protocol'])
            contractors.append(device['snmp']['privacy-passphrase'])

    checks = map(check, zip(contracts, contractors))
    falses = [check['error'] for check in checks if not check['valid?']]

    notes  = {'note' : falses} if any(falses) else {}
    report['check'] = {'status' : 'invalid' if any(falses) else 'valid'} | notes
    reports.append(report)
    return reports

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as system:
        config  = json.loads(system.read())
        devices = functools.reduce(check_device,config['device'],[])

        report = config | {'device' : devices}
        print(json.dumps(report))
