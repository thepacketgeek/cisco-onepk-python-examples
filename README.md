cisco-onepk-python-examples
===========================

Examples of using the Cisco OnePK python SDK to go along with my [blog series here](http://thepacketgeek.com/series/cisco-onepk/)

## Setting up your Cisco IOS device for OnePK

In order to use the OnePK SDK with a network element, you must enable onep on the Cisco IOS device:
	
	HostName(config)# username [username] privilege-level 15 secret [secret]
    HostName(config)# onep
    HostName(config-onep)#transport type tls disable-remotecert-validation

Note that this config along with the TLS pinning I use in the example scripts do not fully verify the certificates. This should not be used in production and are only used in order to get you up to speed with OnePL quickly. For proper production-ready cert deployment steps please visit: https://developer.cisco.com/media/TLS_Pinning_and_Debugging_Tech_Note/GUID-354FCB46-EA02-4315-8681-583C177357F4.html


