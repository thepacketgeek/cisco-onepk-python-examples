#############
# Onep_Connect module
# written by thePacketGeek (thepacketgeek.com)
# 
# This is a module used to connect to a 
# onep network element and returns the 
# NetworkElement object.
#
# Dependencies:
# onep
# 
# Network Element Config
# In order to use onep with a Cisco IOS device, you must enable onep
# 
# HostName(config)# username [username] privilege-level 15 secret [secret]
# HostName(config)# onep
# HostName(config-onep)# transport mode tls disable-remotecert-validation
#############

# Import the onePK Libraries  
from onep.element.NetworkElement import NetworkElement  
from onep.element.SessionConfig import SessionConfig
from onep.core.util import tlspinning, HostIpCheck  
from onep.core.exception.OnepConnectionException import OnepConnectionException
  
def connect(ne_addr, ne_username, ne_password):

	# check to see if ne_addr is a valid IP(v6) address
	if not (HostIpCheck(ne_addr).is_ipv4() or HostIpCheck(ne_addr).is_ipv6()):
		raise ValueError('%s is not a valid IP address' % ne_addr)	

	# TLS Connection (This is the TLS Pinning Handler)  
	class PinningHandler(tlspinning.TLSUnverifiedElementHandler):  
	   def __init__(self, pinning_file):  
	       self.pinning_file = pinning_file  
	   def handle_verify(self, host, hashtype, finger_print, changed):  
	       return tlspinning.DecisionType.ACCEPT_ONCE  
	  
	# Connection to my onePK enabled Network Element  
	config = SessionConfig(None)  
	config.set_tls_pinning('', PinningHandler(''))  
	config.transportMode = SessionConfig.SessionTransportMode.TLS  
	network_element = NetworkElement(ne_addr)

	# Try authenticating, raise error if unsuccessful  
	try:
		network_element.connect(ne_username, ne_password, config)  
	except OnepConnectionException:
		raise ValueError('Invalid Credentials or unable to reach %s.' % network_element)  

	return network_element