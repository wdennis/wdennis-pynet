#!/usr/bin/env python

__author__ = 'Will Dennis'
__email__ = 'wdennis@nec-labs.com'

from snmp_helper import snmp_get_oid, snmp_extract


ROUTER_LIST = [('50.242.94.227', 'galileo', 7961), ('50.242.94.227', 'galileo', 8061)]

OID_LIST = ['1.3.6.1.2.1.1.5.0', '1.3.6.1.2.1.1.1.0']


def get_router_info(this_router, this_oid):
    return snmp_extract(snmp_get_oid(this_router, oid=this_oid))


for router in ROUTER_LIST:
    for oid in OID_LIST:
        output = get_router_info(router, oid)
        print("\n{}\n".format(output))
