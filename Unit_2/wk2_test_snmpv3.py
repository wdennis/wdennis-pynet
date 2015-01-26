#!/usr/bin/env python

__author__ = 'Will Dennis'
__email__ = 'willard.dennis@gmail.com'

import snmp_helper


# OID parameters
oid_ifEntry = '1.3.6.1.2.1.2.2.1'
ifDescr = '2'
ifAdminStatus = '7'
ifOperStatus = '8'
ifInOctets = '10'
ifInUcastPkts = '11'
ifInDiscards = '13'
ifInErrors = '14'
ifInUnknownProtos = '15'
ifOutOctets = '16'
ifOutUcastPkts = '17'
ifOutDiscards = '19'
ifOutErrors = '20'

# SNMPv3 parameters
snmpv3_user = 'pysnmp'
snmpv3_authkey = 'galileo1'
snmpv3_encryptkey = 'galileo1'

# Target device
target_ip_addr = '50.242.94.227'
target_ifIndex = '5'

snmpv3_credentials = (snmpv3_user, snmpv3_authkey, snmpv3_encryptkey)

pynet_rtr1 = (target_ip_addr, 7961)
pynet_rtr2 = (target_ip_addr, 8061)

oid_to_get = oid_ifEntry + "." + ifOutOctets + "." + target_ifIndex

snmp_data = snmp_helper.snmp_get_oid_v3(pynet_rtr1, snmpv3_credentials, oid=oid_to_get)
output = snmp_helper.snmp_extract(snmp_data)
print(output)