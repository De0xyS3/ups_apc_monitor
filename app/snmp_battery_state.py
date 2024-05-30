from pysnmp.hlapi import *

def get_snmp_battery_state():
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('apc', mpModel=0),
               UdpTransportTarget(('192.168.1.10', 161)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.4.1.318.1.1.1.2.2.1.0')))
    )
    if errorIndication:
        return f'Error: {errorIndication}'
    elif errorStatus:
        return f'Error: {errorStatus}'
    else:
        return varBinds[0][1]
