# Akamon #

Generates, validates, and tests monitoring configurations.

## I would like to setup my monitoring; what should I do?

* Generate a configuration
* Edit the configuration
* Check the configuration is valid
* Test the configuration.

### Generate a configuration
By default, the command generates a template of one device:
```
$ make config device=1 | python3 -mjson.tool --indent=2 | tee --append config.json
{
  "name": "EK5Wr36R",
  "id": "tiPTtjXH",
  "device": [
    {
      "name": "Rvd5i8as",
      "ip": "58.141.183.139",
      "username": "admin",
      "password": "",
      "type": "FMG",
      "snmp": {
        "version": "3",
        "community": "",
        "username": "oRQ0",
        "security-level": "authNoPriv",
        "authentication-protocol": "SHA",
        "authentication-password": "zgjW",
        "privacy-protocol": "",
        "privacy-passphrase": ""
      }
    }
  ]
}
```

### Edit the configuration
Save the configuration as _config.json;_ then it is seeable by the script.
```
$ make info
{
  "name": "EK5Wr36R",
  "id": "tiPTtjXH",
  "device": [
    {
      "name": "F6KF31-4",
      "ip": "1003.5.56.238",
      "username": "admin",
      "password": "",
      "type": "FGT",
      "snmp": {
        "version": "3",
        "community": "2KZh",
        "username": "",
        "security-level": "noAuthNoPriv",
        "authentication-protocol": "",
        "authentication-password": "",
        "privacy-protocol": "",
        "privacy-passphrase": ""
      }
    }
  ]
}
```

### Check the configuration is valid
Before proceeding any further, check the configuration:
```
$ make check
{
  "name": "EK5Wr36R",
  "id": "tiPTtjXH",
  "device": [
    {
      "name": "F6KF31-4",
      "ip": "1003.5.56.238",
      "check": {
        "status": "invalid",
        "note": [
          "Invalid IPv4 address",
          "Username should be non-empty string"
        ]
      }
    }
  ]
}

$ make info
{
  "name": "EK5Wr36R",
  "id": "tiPTtjXH",
  "device": [
    {
      "name": "F6KF31-4",
      "ip": "10.5.56.238",
      "username": "admin",
      "password": "",
      "type": "FGT",
      "snmp": {
        "version": "3",
        "community": "2KZh",
        "username": "2KZh",
        "security-level": "noAuthNoPriv",
        "authentication-protocol": "",
        "authentication-password": "",
        "privacy-protocol": "",
        "privacy-passphrase": ""
      }
    }
  ]
}

$ make check
{
  "name": "EK5Wr36R",
  "id": "tiPTtjXH",
  "device": [
    {
      "name": "F6KF31-4",
      "ip": "10.5.56.238",
      "check": {
        "status": "valid"
      }
    }
  ]
}
```

### Test the monitoring
When done, test the configuration. This command does install the configuration, and test it may reach the devices.
```
$ make test | python3 -mjson.tool --indent=2
{
  "time": "2022-10-31T15:30:34+0100",
  "message": "test",
  "id": "60c58929-11ee-437e-a3f8-7e10df9bd6da",
  "device": "F6KF31-4",
  "command": {
    "input": "snmpwalk -v2c -c 2KZh 10.5.56.238 system",
    "output": "SNMPv2-MIB::sysDescr.0 = STRING: FG-EVI_01_A\nSNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.12356.101.1.60001\nDISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (218693076) 25 days, 7:28:50.76\nSNMPv2-MIB::sysContact.0 = STRING: nx@acme.com\nSNMPv2-MIB::sysName.0 = STRING: FG-EVI_01_A/F6KF31T019900199\nSNMPv2-MIB::sysLocation.0 = STRING: EQ7\nSNMPv2-MIB::sysServices.0 = INTEGER: 78\nSNMPv2-MIB::sysORLastChange.0 = Timeticks: (0) 0:00:00.00\nSNMPv2-MIB::sysORIndex.1 = INTEGER: 1\nSNMPv2-MIB::sysORID.1 = OID: SNMPv2-SMI::zeroDotZero.0\nSNMPv2-MIB::sysORDescr.1 = STRING: \nSNMPv2-MIB::sysORUpTime.1 = Timeticks: (0) 0:00:00.00\n"
  }
}
```

## I would like to change my monitoring; what should I do?

* Clean the running monitoring
* Edit the configuration
* Test the new configuration.

For instance; we will change the monitoring from SNMPv2 to SNMPv3.
```
$ make clean
{"time": "2022-10-31T15:32:53+0100", "message": "clean", "id": "d2799096-5657-4caa-9668-530a9ea84a9e", "config": {"name": "Rvd5i8as", "id": "tiPTtjXH", "device": [{"name": "F6KF31-4", "ip": "10.5.56.238", "username": "admin", "password": "", "type": "FGT", "snmp": {"version": "2", "community": "2KZh", "username": "2KZh", "security-level": "noAuthNoPriv", "authentication-protocol": "", "authentication-password": "", "privacy-protocol": "", "privacy-passphrase": ""}}]}}

$ make info
{
  "name": "EK5Wr36R",
  "id": "tiPTtjXH",
  "device": [
    {
      "name": "F6KF31-4",
      "ip": "10.5.56.238",
      "username": "admin",
      "password": "",
      "type": "FGT",
      "snmp": {
        "version": "3",
        "community": "2KZh",
        "username": "2KZh",
        "security-level": "noAuthNoPriv",
        "authentication-protocol": "",
        "authentication-password": "",
        "privacy-protocol": "",
        "privacy-passphrase": ""
      }
    }
  ]
}

$ make check
{
  "name": "EK5Wr36R",
  "id": "tiPTtjXH",
  "device": [
    {
      "name": "F6KF31-4",
      "ip": "10.5.56.238",
      "check": {
        "status": "valid"
      }
    }
  ]
}

$ make test | python3 -mjson.tool --indent=2
{
  "time": "2022-10-31T15:34:11+0100",
  "message": "test",
  "id": "c27079a7-6618-4fca-991f-9ece71884cac",
  "device": "F6KF31-4",
  "command": {
    "input": "snmpwalk -v3 -l noAuthNoPriv -u 2KZh 10.5.56.238 system",
    "output": "SNMPv2-MIB::sysDescr.0 = STRING: FG-EVI_01_A\nSNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.12356.101.1.60001\nDISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (218714779) 25 days, 7:32:27.79\nSNMPv2-MIB::sysContact.0 = STRING: nx@acme.com\nSNMPv2-MIB::sysName.0 = STRING: FG-EVI_01_A/F6KF31T019900199\nSNMPv2-MIB::sysLocation.0 = STRING: EQ7\nSNMPv2-MIB::sysServices.0 = INTEGER: 78\nSNMPv2-MIB::sysORLastChange.0 = Timeticks: (0) 0:00:00.00\nSNMPv2-MIB::sysORIndex.1 = INTEGER: 1\nSNMPv2-MIB::sysORID.1 = OID: SNMPv2-SMI::zeroDotZero.0\nSNMPv2-MIB::sysORDescr.1 = STRING: \nSNMPv2-MIB::sysORUpTime.1 = Timeticks: (0) 0:00:00.00\n"
  }
}
```

## What have I been doing?
A journal logs all the activities that did affect the monitoring:
```
$ make log
{"time": "2022-10-31T15:30:30+0100", "message": "build", "id": "6c241104-4aa8-4741-86a1-b266d73596f8", "config": {"container": {"id": "f44e22d0c8a403b92e5c7e9f96a50923ffe642afbdce003bc925c750ef9dd728", "image": "cmon:betav3", "name": "sqvalcmontiPTtjXH", "host": "sqvalcmontiPTtjXH"}, "name": "Rvd5i8as", "id": "tiPTtjXH", "device": [{"name": "F6KF31-4", "ip": "10.5.56.238", "username": "admin", "password": "", "type": "FGT", "snmp": {"version": "2", "community": "2KZh", "username": "2KZh", "security-level": "noAuthNoPriv", "authentication-protocol": "", "authentication-password": "", "privacy-protocol": "", "privacy-passphrase": ""}}]}}
{"time": "2022-10-31T15:30:34+0100", "message": "install", "id": "f90bffb6-9d49-48e0-bcfe-1474c12cf7cd", "config": {"container": {"id": "f44e22d0c8a403b92e5c7e9f96a50923ffe642afbdce003bc925c750ef9dd728", "image": "cmon:betav3", "name": "sqvalcmontiPTtjXH", "host": "sqvalcmontiPTtjXH"}, "name": "Rvd5i8as", "id": "tiPTtjXH", "device": [{"name": "F6KF31-4", "ip": "10.5.56.238", "username": "admin", "password": "", "type": "FGT", "snmp": {"version": "2", "community": "2KZh", "username": "2KZh", "security-level": "noAuthNoPriv", "authentication-protocol": "", "authentication-password": "", "privacy-protocol": "", "privacy-passphrase": ""}}]}}
{"time": "2022-10-31T15:32:53+0100", "message": "clean", "id": "d2799096-5657-4caa-9668-530a9ea84a9e", "config": {"name": "Rvd5i8as", "id": "tiPTtjXH", "device": [{"name": "F6KF31-4", "ip": "10.5.56.238", "username": "admin", "password": "", "type": "FGT", "snmp": {"version": "2", "community": "2KZh", "username": "2KZh", "security-level": "noAuthNoPriv", "authentication-protocol": "", "authentication-password": "", "privacy-protocol": "", "privacy-passphrase": ""}}]}}
{"time": "2022-10-31T15:34:07+0100", "message": "build", "id": "fb5c454c-09ec-4d7f-8560-c71cdcd4bb7a", "config": {"container": {"id": "895f378b3e0fc001ed87b6e0f02b23188bc4cc16b55fa094c06d889b04042681", "image": "cmon:betav3", "name": "sqvalcmontiPTtjXH", "host": "sqvalcmontiPTtjXH"}, "name": "Rvd5i8as", "id": "tiPTtjXH", "device": [{"name": "F6KF31-4", "ip": "10.5.56.238", "username": "admin", "password": "", "type": "FGT", "snmp": {"version": "3", "community": "2KZh", "username": "2KZh", "security-level": "noAuthNoPriv", "authentication-protocol": "", "authentication-password": "", "privacy-protocol": "", "privacy-passphrase": ""}}]}}
{"time": "2022-10-31T15:34:11+0100", "message": "install", "id": "e6083253-0980-4368-bbe3-346c8ad8df93", "config": {"container": {"id": "895f378b3e0fc001ed87b6e0f02b23188bc4cc16b55fa094c06d889b04042681", "image": "cmon:betav3", "name": "sqvalcmontiPTtjXH", "host": "sqvalcmontiPTtjXH"}, "name": "Rvd5i8as", "id": "tiPTtjXH", "device": [{"name": "F6KF31-4", "ip": "10.5.56.238", "username": "admin", "password": "", "type": "FGT", "snmp": {"version": "3", "community": "2KZh", "username": "2KZh", "security-level": "noAuthNoPriv", "authentication-protocol": "", "authentication-password": "", "privacy-protocol": "", "privacy-passphrase": ""}}]}}
```

## In fact; what has happened?
The monitoring creates a container, and sets it up with your configuration. After a test is done, you may as well log into the container.
```
$ make login
root@sqvalcmontiPTtjXH:~# 
```
