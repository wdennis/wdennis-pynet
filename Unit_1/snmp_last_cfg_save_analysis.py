#!/usr/bin/env python

__author__ = 'Will Dennis'
__email__ = 'wdennis@nec-labs.com'

from snmp_helper import snmp_get_oid, snmp_extract


ROUTER_INFO = ('50.242.94.227', 'galileo', 7961)

OID_LIST = ['1.3.6.1.2.1.1.3.0', '1.3.6.1.4.1.9.9.43.1.1.1.0', '1.3.6.1.4.1.9.9.43.1.1.2.0',
            '1.3.6.1.4.1.9.9.43.1.1.3.0']


def get_router_info(this_router, this_oid):
    return snmp_extract(snmp_get_oid(this_router, oid=this_oid))


def convert_to_secs(timeticks):
    return timeticks / 100.0


oid_value_list = []
for curr_oid in OID_LIST:
    oid_value_list.append(float(get_router_info(ROUTER_INFO, curr_oid)))
sysUptime, ccmHistoryRunningLastChanged, ccmHistoryRunningLastSaved, ccmHistoryStartupLastChanged = oid_value_list

print("System has been up for {} seconds".format(convert_to_secs(sysUptime)))
print("Last running config change was at {} seconds since boot.".format(convert_to_secs(ccmHistoryRunningLastChanged)))
print("Last running config save was at {} seconds since boot.".format(convert_to_secs(ccmHistoryRunningLastSaved)))
print("Last startup config change was at {} seconds since boot.".format(convert_to_secs(ccmHistoryStartupLastChanged)))

if ccmHistoryStartupLastChanged > 0:
    tics_since_last_change = (sysUptime - ccmHistoryRunningLastChanged)
    tics_since_last_save = (sysUptime - ccmHistoryStartupLastChanged)
    if tics_since_last_save > tics_since_last_change:
        print(
        "Last running config change {} seconds after last save;\nPlease issue the 'copy run start' command!".format(
            convert_to_secs(tics_since_last_save - tics_since_last_change))
        )
    else:
        print("Startup config in sync with Running config.")
else:
    print("Startup config has not been saved since the last system boot.")
    if ccmHistoryRunningLastChanged > 0:
        print("The running config has been updated since boot time, so please issue the 'copy run start' command!")
    else:
        print("However, the running config has not changed since boot, so no action needs taken.")
