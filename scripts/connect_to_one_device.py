# Example script of connecting to a OnePK Network Element
#
# Uses TLS Pinning to get around installing valid certs
# Not recommended for production use. 
# Read more: https://communities.cisco.com/message/156836#156836

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
ne = NetworkElement('1.1.1.1', 'App_Name')  
ne.connect('username', 'password', config)  

try:  
	# Print the information of the Network Element  
	print ne

finally:
	# Finally have the application disconnect from the Network Element  
	ne.disconnect() 
