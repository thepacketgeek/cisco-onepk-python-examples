# OneP script to set an interface IP address (located by name)
# 
# Usage:
#  python script_name.py [ip_address] [username] [password] [interface_name] [ip/prefix]


# This script uses the onep_connect.py module
from onep_connect import connect
from onep.core.util import OnepConstants
from onep.core.util import HostIpCheck
import sys

if len(sys.argv) < 5:
    print 'Usage: python script_name.py [ip_address] [username] [password] [interface_name] [ip/prefix]'
    quit()

# Connect using passed in connection values
# (will raise a ValueError if bad IP address or credentials)
ne = connect(sys.argv[1], sys.argv[2], sys.argv[3])

try:  
    #separate IP and prefix
    ip_address, ip_prefix = sys.argv[5].split('/')
    
    # Test for IPv4 or IPv6 address and assign accordingly
    if HostIpCheck(ip_address).is_ipv4():
        scope_type = OnepConstants.OnepAddressScopeType.ONEP_ADDRESS_IPv4_PRIMARY
        if not (0 < int(ip_prefix) <= 32):
            raise ValueError('%s is not a valid IPv4 prefix' % ip_prefix)

    elif HostIpCheck(ip_address).is_ipv6():
        scope_type = OnepConstants.OnepAddressScopeType.ONEP_ADDRESS_IPv6_ALL
        if not (0 < int(ip_prefix) <= 32):
            raise ValueError('%s is not a valid IPv6 prefix' % ip_prefix)
    else:
        raise ValueError('%s is not a valid IP address' % ip_address)
        
    #get interface by name
    try:
        iface = ne.get_interface_by_name(sys.argv[4])
    except:
        raise ValueError('The \'%s\' interface does not exist on this Network Element.' % sys.argv[4])

    iface.set_address(1, scope_type, ip_address, int(ip_prefix))

    print 'The %s interface has been configured with the address: %s' % (sys.argv[4], sys.argv[5])

finally:
    # Finally have the application disconnect from the Network Element  
    ne.disconnect() 


## Output:
# $ python set_interface_address.py 10.211.55.200 admin admin lo0 1.1.1.10/32
# The Lo0 interface has been configured with the address: 1.1.1.10/32