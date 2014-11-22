from onep_connect import connect
from onep.core.util import HostIpCheck
from onep.core.util import OnepConstants
from onep.policy import Acl, L3Acl, L3Ace

# Example Syslog message from IDS
syslog_message = 'Mar 29 2014 09:54:18: %IDS-9-ATTACK: Detected TCP attack from 198.207.223.240/53337 to 10.10.20.15/22 on Int: GigabitEthernet2'

def create_dynamic_ace(sequence, permit, syslog):
    ''' Build ACE from syslog message

    sequence (int): Sequence number of ACE to insert in ACL
    permit (bool): True == permit, False == deny
    syslog (str): Syslog message, IP Address order is assumed.
    '''

    ip_addresses = [x for x in syslog.split(' ') if HostIpCheck(x.split('/')[0]).is_ipv4()]
    protocol = [x for x in syslog.split(' ') if x in ['TCP', 'UDP', 'IP']][0]

    # Create ACE that matches the syslog addresses
    l3_ace = L3Ace(sequence, permit)
    if protocol.lower() == 'tcp': 
        l3_ace.protocol = OnepConstants.AclProtocol.TCP
    if protocol.lower() == 'udp': 
        l3_ace.protocol = OnepConstants.AclProtocol.UDP
    if protocol.lower() == 'ip': 
        l3_ace.protocol = OnepConstants.AclProtocol.IP
    
    l3_ace.dst_prefix = ip_addresses[1].split('/')[0]
    l3_ace.dst_prefix_len = 32
    dst_port = int(ip_addresses[1].split('/')[1])
    l3_ace.set_dst_port_range(dst_port, dst_port)

    l3_ace.src_prefix = ip_addresses[0].split('/')[0]
    l3_ace.src_prefix_len = 32
    src_port = int(ip_addresses[0].split('/')[1])
    l3_ace.set_src_port_range(src_port, src_port)

    return l3_ace

try:
    # Connect to a router inline with the attacker's traffic
    ne = connect('1.1.1.1', 'admin', 'admin')

    #specify the interface towards the attacker
    interface = ne.get_interface_by_name('gi2')

    #  Create a IPv4 L3 ACL
    l3_acl = L3Acl(ne, OnepConstants.OnepAddressFamilyType.ONEP_AF_INET, L3Acl.OnepLifetime.ONEP_PERSISTENT)

    # Run function to create ACE based on syslog addresses
    l3_ace_10 = create_dynamic_ace(10, False, syslog_message)

    # Create ACE to allow all other traffic
    l3_ace_20 = L3Ace(20, True)  #True == permit
    l3_ace_20.protocol = OnepConstants.AclProtocol.ALL
    l3_ace_20.set_src_prefix_any()
    l3_ace_20.set_dst_prefix_any()

    # Add both ACEs to the ACL
    l3_acl.add_ace(l3_ace_10)
    l3_acl.add_ace(l3_ace_20)

    # Apply the ACL to the interface
    interface = ne.get_interface_by_name(syslog_message.split(' ')[-1])
    l3_acl.apply_to_interface(interface, Acl.Direction.ONEP_DIRECTION_IN)

    print 'ACL created and applied to the %s interface' % interface.name


finally:
    # End the onep session (ACL remains because we used a persistent lifetime)
    ne.disconnect()




