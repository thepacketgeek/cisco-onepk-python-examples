# Import the onePK Libraries  
from onep.element.NetworkElement import NetworkElement  
from onep.element.SessionConfig import SessionConfig
from onep.core.util import tlspinning  
from onep.interfaces import InterfaceFilter 
  
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
ne = NetworkElement('10.211.55.200', 'HelloWorld')  
ne.connect('admin', 'admin', config)  

try:  
	# Print the information of the Network Element  
	print ne

	print '\n'

	#Create Interface Filter and print interface list
	if_filter = InterfaceFilter(interface_type=1)
	for interface in ne.get_interface_list(if_filter):
		print interface.get_config()
		print '\n%s: %s\n' % (interface.name, interface.get_address_list())
	  
finally:
	# Finally have the application disconnect from the Network Element  
	ne.disconnect() 
