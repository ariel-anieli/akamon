import functools
import json
import sys

def auth_proto():
    return {
        'term'     : lambda auth: auth in ['MD5', 'SHA'],
        'error'    : 'Authentication protocol is either MD5 or SHA',
        'severity' : 'minor'
    }

def auth_pswd():
    return {
        'term'     : lambda name: isinstance(name, str) and len(name)>0,
        'error'    : 'Authentication password should be non-empty string',
        'severity' : 'minor'
    }

def community():
    return {
        'term'     : lambda comm: isinstance(comm, str) and len(comm)>0,
        'error'    : 'Community name should be non-empty string',
        'severity' : 'minor'
    }

def is_ipv4(addr):
    return len(addr.split('.'))==4 \
        and all([int(byte)<256 and int(byte)>=0 for byte in addr.split('.')])

def ip():
    return {
        'term'     : lambda addr: is_ipv4(addr),
        'error'    : 'Invalid IPv4 address',
        'severity' : 'major'
    }

def name():
    return {
        'term'     : lambda name: isinstance(name, str) and len(name)>0,
        'error'    : 'Device name should be non-empty string',
        'severity' : 'minor'
    }

def priv_proto():
    return {
        'term'     : lambda auth: auth in ['AES', 'DES'],
        'error'    : 'Privacy protocol is either AES or DES',
        'severity' : 'minor'
    }

def priv_pass():
    return {
        'term'     : lambda name: isinstance(name, str) and len(name)>0,
        'error'    : 'Privacy passphrase should be non-empty string',
        'severity' : 'minor'
    }

def security_level():
    return {
        'term'     : lambda sec: sec in ['authPriv','authNoPriv','noAuthNoPriv'],
        'error'    : 'Security level is either'
                     'authPriv, authNoPriv, noAuthNoPriv',
        'severity' : 'major'
    }

def username():
    return {
        'term'     : lambda user: isinstance(user, str) and len(user)>0,
        'error'    : 'Username should be non-empty string',
        'severity' : 'minor'
    }

def version():
    return {
        'term'     : lambda version: version in ['1', '2', '3'],
        'error'    : 'SNMP version must be 1, 2, or 3',
        'severity' : 'major'
    }

def check(agreement):
    contract, contractor = agreement
    return {
        'valid?'   : contract['term'](contractor),
        'error'    : contract['error'],
        'severity' : contract['severity']
    }

def check_device(reports, device):
    report      = {'name' : device['name'],
                   'ip'   : device['ip']}
    contracts   = [version(), ip(), name()]
    contractors = [device['snmp']['version'], device['ip'], device['name']]

    match device['snmp']['version']:
        case '1' | '2':
            contracts.append(community())
            contractors.append(device['snmp']['community'])
        case '3':
            contracts.append(security_level())
            contractors.append(device['snmp']['security-level'])

            match device['snmp']['security-level']:
                case 'noAuthNoPriv':
                    contracts.append(username())
                    contractors.append(device['snmp']['username'])
                case 'authNoPriv':
                    contracts.append(username())
                    contracts.append(auth_proto())
                    contracts.append(auth_pswd())

                    contractors.append(device['snmp']['username'])
                    contractors.append(device['snmp']['authentication-protocol'])
                    contractors.append(device['snmp']['authentication-password'])
                case 'authPriv':
                    contracts.append(username())
                    contracts.append(auth_proto())
                    contracts.append(auth_pswd())
                    contracts.append(priv_proto())
                    contracts.append(priv_pass())

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
