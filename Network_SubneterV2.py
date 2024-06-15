import ipaddress
import math

def get_address():
    while True:
        address = input("Enter the network address: ")
        try:
            network = ipaddress.IPv4Network(address, strict=False)
            print('Network address:', network)
            return network
        except ValueError:
            print('Invalid address/netmask for IPv4:', address)

def get_mode():
    while True:
        mode = input("What mode do you want to use to segment this network (VLSM or FLSM): ").strip().upper()
        if mode in ['VLSM', 'FLSM']:
            print(f'The mode you chose is {mode}.')
            return mode
        else:
            print('Please, enter a valid mode (VLSM or FLSM).')

def get_subnet_num():
    while True:
        subnet_num = input('How many subnets are in this network: ')
        if subnet_num.isdigit() and int(subnet_num) > 0:
            print('The number of subnets in this network is:', subnet_num)
            return int(subnet_num)
        else:
            print('Please enter a valid number of subnets (greater than 0).')

def get_subnet_host_counts_vlsm(subnet_num):
    subnet_host_counts = []
    for i in range(subnet_num):
        while True:
            host_num = input(f'How many hosts are in Subnet {i + 1}: ')
            if host_num.isdigit() and int(host_num) > 0:
                subnet_host_counts.append(int(host_num))
                break
            else:
                print('Please enter a valid number of hosts (greater than 0).')
    subnet_host_counts.sort(reverse=True)
    print('The number of hosts in each subnet are:', subnet_host_counts)
    return subnet_host_counts

def get_subnet_host_counts_flsm(subnet_num):
    max_host_num = 0
    for i in range(subnet_num):
        while True:
            try:
                host_num = int(input(f'How many hosts are in Subnet {i + 1}: '))
                if host_num > 0:
                    max_host_num = max(max_host_num, host_num)
                    break
                else:
                    print('Please enter a valid number of hosts (greater than 0).')
            except ValueError:
                print('Please enter a valid integer.')
    subnet_host_counts = [max_host_num] * subnet_num
    print('The highest number of hosts entered in any subnet is:', max_host_num)
    return subnet_host_counts

def get_mask(network):
    return network.prefixlen

def get_ip_address(network):
    return network.network_address

def get_subnet_host_bits(subnet_host_counts):
    subnet_host_bits = [int(math.ceil(math.log2(count + 2))) for count in subnet_host_counts]
    print('The host bits of subnets are:', subnet_host_bits)
    return subnet_host_bits

def get_subnets_mask(mask, subnet_host_bits):
    subnets_mask = [mask + ((32 - mask) - bits) for bits in subnet_host_bits]
    print('The subnets masks for this network are:', subnets_mask)
    return subnets_mask

def get_subnets(network, subnets_mask):
    subnets = []
    address = get_ip_address(network)
    for mask in subnets_mask:
        subnet = ipaddress.ip_network(f'{address}/{mask}', strict=False)
        subnets.append(subnet)
        address = subnet.network_address + subnet.num_addresses
    return subnets

def get_subnet_info(subnets):
    subnets_info = []
    for subnet in subnets:
        info = {
            'network_address': subnet.network_address,
            'netmask': subnet.netmask,
            'first_host': subnet.network_address + 1,
            'last_host': subnet.broadcast_address - 1,
            'broadcast_address': subnet.broadcast_address,
            'host_count': subnet.num_addresses - 2
        }
        subnets_info.append(info)
    return subnets_info

def display_subnet_info(subnets_info):
    for idx, info in enumerate(subnets_info, start=1):
        print(f'Subnet {idx} Information:')
        print(f'  Network Address: {info["network_address"]}')
        print(f'  Netmask: {info["netmask"]}')
        print(f'  First Host: {info["first_host"]}')
        print(f'  Last Host: {info["last_host"]}')
        print(f'  Broadcast Address: {info["broadcast_address"]}')
        print(f'  Number of Hosts: {info["host_count"]}')
        print()

def main():
    while True:
        network = get_address()
        mask = get_mask(network)
        mode = get_mode()
        
        if mode == 'VLSM':
            subnet_num = get_subnet_num()
            subnet_host_counts = get_subnet_host_counts_vlsm(subnet_num)
        else:
            subnet_num = get_subnet_num()
            subnet_host_counts = get_subnet_host_counts_flsm(subnet_num)
        
        subnet_host_bits = get_subnet_host_bits(subnet_host_counts)
        subnets_mask = get_subnets_mask(mask, subnet_host_bits)
        subnets = get_subnets(network, subnets_mask)
        subnets_info = get_subnet_info(subnets)
        display_subnet_info(subnets_info)
        
        cont = input('Do you want to subnet another network? (yes or no): ').strip().lower()
        if not cont.startswith('y'):
            print('Thanks for using our script!')
            break

if __name__ == "__main__":
    main()
