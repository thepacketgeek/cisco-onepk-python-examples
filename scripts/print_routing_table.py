# OneP script to print interfaces with associated IPv4/IPv6 addresses
# 
# Usage:
#  python script_name.py [ip_address] [username] [password]


# This script uses the onep_connect.py module
from onep_connect import connect
from onep.routing import RIB, Routing, L3UnicastScope, L3UnicastRouteRange, L3UnicastRIBFilter, RouteRange, AppRouteTable
from onep.interfaces import NetworkPrefix
import sys

if len(sys.argv) != 4:
	print 'Usage: python script_name.py [ip_address] [username] [password]'
	quit()

# Connect using passed in connection values
# (will raise a ValueError if bad IP address or credentials)
ne = connect(sys.argv[1], sys.argv[2], sys.argv[3])

try:  
	routing = Routing.get_instance(ne)

	# We need to get routes separately for IPv4 and IPv6
	# since we can't specify a Scope.AFIType of both address families :(
	for afi_type in (L3UnicastScope.AFIType.IPV4, L3UnicastScope.AFIType.IPV6):
		prefix = NetworkPrefix("::", 0)
		scope = L3UnicastScope("", afi_type)
		range = L3UnicastRouteRange(
		              prefix, RouteRange.RangeType.EQUAL_OR_LARGER, 0)
		filter = L3UnicastRIBFilter()
		route_list = routing.rib.get_route_list(scope, filter, range)

		for route in route_list:
			#get the first next hop only, either the interface or IP
			for next_hop in route.next_hop_list:
				next_hop = max([next_hop.address, next_hop.network_interface.name], key=len)
				break
			
			full_prefix = '%s/%s' % (route.prefix.address, route.prefix.prefix_length)
			print('%-24s  Type: %-12s AD: %-4s Metric: %-3s Next-Hop: %-20s') % \
				(full_prefix, route.OwnerType.enumval(route.owner_type), route.admin_distance, 
					route.metric, next_hop)

finally:
	# Finally have the application disconnect from the Network Element  
	ne.disconnect() 



## Output:
# thePacketGeek$ python print_routing_table.py 10.211.55.200 admin admin
# 0.0.0.0/0                 Type: STATIC       AD: 1    Metric: 0   Next-Hop: 10.211.55.1
# 0.0.0.0/0                 Type: STATIC       AD: 1    Metric: 0   Next-Hop: 10.211.55.1
# 1.1.1.1/32                Type: LOCAL        AD: 0    Metric: 0   Next-Hop: Loopback0
# 10.211.55.0/24            Type: CONNECTED    AD: 0    Metric: 0   Next-Hop: GigabitEthernet1
# 10.211.55.200/32          Type: LOCAL        AD: 0    Metric: 0   Next-Hop: GigabitEthernet1
# 172.16.0.0/16             Type: STATIC       AD: 1    Metric: 0   Next-Hop: 192.168.56.10
# 192.168.56.0/24           Type: CONNECTED    AD: 0    Metric: 0   Next-Hop: GigabitEthernet2
# 192.168.56.1/32           Type: LOCAL        AD: 0    Metric: 0   Next-Hop: GigabitEthernet2
# 2001:56::/64              Type: CONNECTED    AD: 0    Metric: 0   Next-Hop: GigabitEthernet2
# 2001:56::1/128            Type: LOCAL        AD: 0    Metric: 0   Next-Hop: GigabitEthernet2
# 2001:100::/64             Type: CONNECTED    AD: 0    Metric: 0   Next-Hop: Loopback0
# 2001:100::1/128           Type: LOCAL        AD: 0    Metric: 0   Next-Hop: Loopback0
# FF00::/8                  Type: LOCAL        AD: 0    Metric: 0   Next-Hop: Null0