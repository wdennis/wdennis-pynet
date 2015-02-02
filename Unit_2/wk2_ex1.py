#!/usr/bin/env python

__author__ = 'Will Dennis'
__email__ = 'wdennis@nec-labs.com'

import json
import datetime

import snmp_helper
from email_helper import send_mail


# Relevant SNMP OIDs
SYS_NAME = '1.3.6.1.2.1.1.5.0'
SYS_UPTIME = '1.3.6.1.2.1.1.3.0'
RUN_LAST_CHANGED = '1.3.6.1.4.1.9.9.43.1.1.1.0'
OIDS_TO_QUERY = [SYS_NAME, SYS_UPTIME, RUN_LAST_CHANGED]

# SNMPv3 parameters
SNMPv3_USER = 'pysnmp'
SNMPv3_AUTHKEY = 'xxxxxx'
SNMPv3_ENCRYPTKEY = 'yyyyyy'
SNMPv3_CREDENTIAL_SET = (SNMPv3_USER, SNMPv3_AUTHKEY, SNMPv3_ENCRYPTKEY)

# Target device parameters
TARGET_IP_ADDR = '10.20.30.40'
PYNET_RTR1 = (TARGET_IP_ADDR, 7961)
PYNET_RTR2 = (TARGET_IP_ADDR, 8061)
ROUTERS_TO_QUERY = [PYNET_RTR1, PYNET_RTR2]

# Email parameters
RECIPIENT = 'willarddennis@gmail.com'
SENDER = 'willarddennis@gmail.com'

for router in ROUTERS_TO_QUERY:
    rtr_query_results = []
    for oid_to_get in OIDS_TO_QUERY:
        snmp_data = snmp_helper.snmp_get_oid_v3(
            router, SNMPv3_CREDENTIAL_SET, oid=oid_to_get)
        output = snmp_helper.snmp_extract(snmp_data)
        rtr_query_results.append(output)

    last_change_delta = int(rtr_query_results[1]) - int(rtr_query_results[2])
    rtr_query_results.append(last_change_delta.__str__())
    filename = rtr_query_results[0] + '.json'
    rtr_fqdn = rtr_query_results[0]

    # Set timestamps
    timenow = datetime.datetime.now()
    last_cfg_change_time = (datetime.datetime.now() - datetime.timedelta(milliseconds=last_change_delta))

    # Read in the contents of the JSON file from last run
    # (if no prior file, use 0's, and JSON file should be created later)
    try:
        with open(filename, 'r') as infile:
            priordata = json.load(infile)
    except IOError:
        print('No prior data file! Will create it on this run.')
        priordata = ['0', '0', '0', '0']

    # Do the comparison between run last changed ticks
    # print(int(rtr_query_results[2]))
    # print(int(priordata[2]))
    if int(rtr_query_results[2]) > int(priordata[2]):
        msg = "{}: Config has changed! Last change was at: {}".format(
            rtr_fqdn, last_cfg_change_time)
        subject = "Config change detected on {}".format(rtr_fqdn)
        send_mail(RECIPIENT, subject, msg, SENDER)
    elif int(rtr_query_results[2]) == int(priordata[2]):
        msg = "{}: No config change from prior run.".format(rtr_fqdn)
    else:
        msg = "Something weird has happened, this run value less than last stored value..."

    print msg

    # Update the JSON file holding the results of this run
    with open(filename, 'w') as outfile:
        json.dump(rtr_query_results, outfile)
