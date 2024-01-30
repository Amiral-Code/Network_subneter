import ipaddress
import math

def get_address():
    while True:
        address = input("Enter the network address: ")
        try:
            network = ipaddress.IPv4Network(address)
            print('Network address:', network)
            return network
        except ValueError:
            print('Invalid address/netmask for IPv4:', address)

def get_mode():
    while True:
        mode = input("What mode do you want to use to segment this network (VLSM or FLSM): ").lower()
        if mode.startswith('v'):
            print('The mode you chose is VLSM.')
            return 'VLSM'
        elif mode.lower().startswith('f'):
            print('The mode you chose is FLSM.')
            return 'FLSM'
        else:
            print('Please, enter a valid mode.')

def get_subnet_num():
    while True:
        subnet_num = input('How many subnets are in this network: ')
        if subnet_num.isdigit():
            print('The number of subnets in this network is:', subnet_num)
            return int(subnet_num)
        else:
            print('Please enter a valid subnets number')

def get_subnet_host_num_vlsm(subnet_num):
    subnet_host_num = []
    for i in range(subnet_num):
        while True:
            host_num = input(f'How many hosts are in Subnet {i + 1}: ')
            if host_num.isdigit() and int(host_num) > 0:
                subnet_host_num.append(int(host_num))
                break
            else:
                print('Please enter a valid number of hosts (greater than 0).')
    subnet_host_num.sort(reverse=True)
    print('The number of hosts in each subnet are:', subnet_host_num)
    return subnet_host_num

def get_subnet_host_num_flsm(subnet_num):
    subnet_host_num = []
    max_host_num = 0  
    for i in range(subnet_num):
        while True:
            try:
                host_num = int(input(f'How many hosts are in Subnet {i + 1}: '))
                if host_num > 0:
                    if host_num > max_host_num:
                        max_host_num = host_num  # Update max_host_num if a higher value is entered
                    break
                else:
                    print('Please enter a valid number of hosts (greater than 0).')
            except ValueError:
                print('Please enter a valid integer.')

    subnet_host_num = [max_host_num] * subnet_num
    print('The highest number of hosts entered in any subnet is:', max_host_num)
    print('The list of hosts in each subnet is:', subnet_host_num)
    return subnet_host_num

def get_mask(network):
    mask = network.prefixlen
    return mask

def get_ip_address(network):
    ip_address = network.network_address
    return ip_address

def get_subnet_host_bits(subnet_host_num):
    subnet_host_bits = [int(math.ceil(math.log2(i + 2))) for i in subnet_host_num]
    print('The host bits of subnets are:', subnet_host_bits)
    return subnet_host_bits

def get_subnets_mask(mask, subnet_host_bits):
    subnets_mask = []
    for i in subnet_host_bits:
        subnet_mask = mask + ((32 - mask) - i)
        subnets_mask.append(subnet_mask)
    print('The subnets masks for this network are:', subnets_mask)
    return subnets_mask

def get_subnets(network, subnets_mask):
    subnets = []
    ip_address = get_ip_address(network)
    address = ip_address
    mask = get_mask(network)

    for i in subnets_mask:
        subnet = ipaddress.ip_network(str(address) + '/' + str(i))
        subnets.append(subnet)
        address = subnet.network_address + subnet.num_addresses
    return subnets

def get_subnet_info(subnets):
    subnets_address = []
    subnets_mask = []
    first_address_ip = []
    last_address_ip = []
    broadcast_address = []
    hosts_num = []
    subnets_info = []
    for i in subnets:
        subnets_address.append(i)
        subnets_mask.append(i.netmask)
        subnet = i.hosts
        first_address_ip.append(i.network_address + 1)
        last_address_ip.append(i.broadcast_address - 1)
        broadcast_address.append(i.broadcast_address)
        hosts_num.append(i.num_addresses - 2)
    
    for j in range(len(subnets)):
        subnets_info.append([subnets_address[j],
        subnets_mask[j],
        first_address_ip[j],
        last_address_ip[j],
        broadcast_address[j],
        hosts_num[j]])
    print()
    return subnets_info

def get_subnet_data(subnets_info):
    x = 1
    for i in subnets_info:
        print(f'subnet{x} address is:', i[0])
        print(f'subnet{x} mask address is:', i[1])
        print(f'subnet{x} first host address is:', i[2])
        print(f'subnet{x} last host address is:', i[3])
        print(f'subnet{x} broadcast address is:', i[4])
        print(f'subnet{x} host number is:', i[5])
        print()
        x += 1

def main():
    while True:
        network = get_address()
        mask = get_mask(network)
        mode = get_mode()
        if mode == 'VLSM':
            subnet_num_vlsm = get_subnet_num()
            subnet_host_num_vlsm = get_subnet_host_num_vlsm(subnet_num_vlsm)
            subnet_host_bits = get_subnet_host_bits(subnet_host_num_vlsm)
            subnets_mask = get_subnets_mask(mask, subnet_host_bits)
            subnets = get_subnets(network, subnets_mask)
            subnets_info = get_subnet_info(subnets)
            subnets_data = get_subnet_data(subnets_info)
            print('Do you want to subnet an other network? (yes or no)')
            if not input('> ').lower().startswith('y'):
                print('Thanks for using our script!')
                break
        else:
            subnet_host_num_flsm = get_subnet_num()
            subnet_host_num_flsm = get_subnet_host_num_flsm(subnet_host_num_flsm)
            subnet_host_bits = get_subnet_host_bits(subnet_host_num_flsm)
            subnets_mask = get_subnets_mask(mask, subnet_host_bits)
            subnets = get_subnets(network, subnets_mask)
            subnets_info = get_subnet_info(subnets)
            subnets_data = get_subnet_data(subnets_info)
            print('Do you want to subnet an other network? (yes or no)')
            if not input('> ').lower().startswith('y'):
                print('Thanks for using our script!')
                break

if __name__ == "__main__":
    main()