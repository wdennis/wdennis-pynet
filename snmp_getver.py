#!/usr/bin/env python

__author__ = 'Will Dennis'
__email__ = 'wdennis@nec-labs.com'

from snmp_helper import snmp_get_oid, snmp_extract


COMMUNITY_STRING = 'galileo'
SNMP_PORT = 7961
TARGET = '50.242.94.227'

DEVICE_FACTS = (TARGET, COMMUNITY_STRING, SNMP_PORT)

OID = '1.3.6.1.2.1.1.1.0'

snmp_data = snmp_get_oid(DEVICE_FACTS, oid=OID)
# print(snmp_data)
output = snmp_extract(snmp_data)

print("Device ver string is: {}".format(output.splitlines()[0]))
