# OneP script to shutdown an interface found by searching for an IP address
# 
# Usage:
#  python script_name.py [ip_address] [username] [password] [ip_to_shutdown] [1/0]


# This script uses the onep_connect.py module
from onep_connect import connect
from onep.interfaces import InterfaceFilter
import sys

if len(sys.argv) < 5:
	print 'Usage: python script_name.py [ip_address] [username] [password] [ip_to_shutdown] [1/0]'
	quit()

# Connect using passed in connection values
# (will raise a ValueError if bad IP address or credentials)
ne = connect(sys.argv[1], sys.argv[2], sys.argv[3])

try:  
	#Create Interface Filter and find interface by IP
	if_filter = InterfaceFilter(interface_type=1)
	for interface in ne.get_interface_list(if_filter):
		if sys.argv[4] in interface.get_address_list():
			# Use passed in shutdown command, or just shutdown
			try:
				interface.shut_down(int(sys.argv[5]))
				if int(sys.argv[5]) == 1:
					print '%s has been shutdown.' % interface.name
				elif int(sys.argv[5]) == 0:
					print '%s has been re-enabled.' % interface.name
			except IndexError, ValueError:
				interface.shut_down(1)
				print '%s has been shutdown.' % interface.name

finally:
	# Finally have the application disconnect from the Network Element  
	ne.disconnect() 



## Output:
# thePacketGeek$ python print_all_interface_IPs.py 10.211.55.200 admin admin 1.1.1.1 1
# Loopback0 has been shutdown.


## Logging on IOS Device
# *Nov 11 20:04:21.030: %ONEP_BASE-6-CONNECT: [Element]: ONEP session Application:noname Host:10.211.55.200 ID:1439 User:admin has connected.
# *Nov 11 20:04:21.038: %SYS-5-CONFIG_I: Configured from 10.211.55.2 by admin on onePK Application: noname ID: 1439
# *Nov 11 20:04:21.045: %ONEP_BASE-6-DISCONNECT: [Element]: ONEP session Application:noname Host:10.211.55.200 ID:1439 User:admin has disconnected.
# *Nov 11 20:04:23.038: %LINEPROTO-5-UPDOWN: Line protocol on Interface Loopback0, changed state to down
# *Nov 11 20:04:23.038: %LINK-5-CHANGED: Interface Loopback0, changed state to administratively down