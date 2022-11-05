import functools
import json
import os
import sys
import re

global_cfg_template = """[global]
customer_name = !name!
project_name  = !pid!
nb_devices    = !devices!
"""

device_cfg_template = """[DUT_!index!]
device_!index!_name               = !name!
device_!index!_ip                 = !ip!
username_!index!                  = !username!
password_!index!                  = !password!
device_!index!_type               = !type!
device_!index!_snmpv              = !snmp-version!
device_!index!_snmp_community     = !snmp-community!
device_!index!_snmp_username      = !snmp-username!
device_!index!_snmp_sec_level     = !snmp-security-level!
device_!index!_snmp_auth_protocol = !snmp-authentication-protocol!
device_!index!_snmp_auth_pass     = !snmp-authentication-password!
device_!index!_snmp_priv_protocol = !snmp-privacy-protocol!
device_!index!_snmp_priv_pass     = !snmp-privacy-passphrase!
"""

def map_device_to_template(item):
    index, device = item
    return [
        ('!index!'                        , str(index)),
        ('!name!'                         , device['name']),
        ('!ip!'                           , device['ip']),
        ('!username!'                     , device['username']),
        ('!password!'                     , device['password']),
        ('!type!'                         , device['type']),
        ('!snmp-version!'                 , device['snmp']['version']),
        ('!snmp-community!'               , device['snmp']['community']),
        ('!snmp-username!'                , device['snmp']['username']),
        ('!snmp-security-level!'          , device['snmp']['security-level']),
        ('!snmp-authentication-protocol!' , device['snmp']['authentication-protocol']),
        ('!snmp-authentication-password!' , device['snmp']['authentication-password']),
        ('!snmp-privacy-protocol!'        , device['snmp']['privacy-protocol']),
        ('!snmp-privacy-passphrase!'      , device['snmp']['privacy-passphrase']),
    ]

def map_global_to_template(config):
    return [
        ('!name!'    , config['name']),
        ('!pid!'     , config['id']),
        ('!devices!' , str(len(config['device']))),
    ]

def configure_device(init, item):

    filled = fill_item_template(device_cfg_template)(
        put_value_in_template,
        map_device_to_template(item)
    )

    return '\n'.join([init, filled])

def put_value_in_template(init, pair):
    key, value = pair
    return re.sub(key, value, init)

def fill_item_template(template):
    return lambda mapper, mapping: functools.reduce(mapper, mapping, template)

if __name__ == "__main__":
    with open(sys.argv[1]) as source:
        config  = json.loads(source.read())
        devices = config['device']
        headers = fill_item_template(global_cfg_template)(
            put_value_in_template,
            map_global_to_template(config)
        )
        monitor = functools.reduce(
            configure_device,
            enumerate(devices, start=1),
            headers
        )

        _file = '/root/master/conf/cmon.ini'
        _id   = config['container']['id']

        cmd   = 'sudo docker exec -it {}'.format(_id)
        cfg   = "sh -c 'echo \"{}\" > {}'".format(monitor, _file)
        start = "sh -c '/root/setup_mon.sh'"
        run   = "sh -c 'service collectd restart'"

        os.system(' '.join([cmd, cfg]))
        os.system(' '.join([cmd, start]))
        os.system(' '.join([cmd, run]))
