def create_subnets(network_address, nb_of_links):
    try:
        octets = (network_address.split('/')[0]).split('.')
        octets[2] = 0
        octets[3] = 0
        plage = f"{octets[0]}.{octets[1]}"
        subnet_addresses = []
        for i in range (nb_of_links):
            subnet_addresses.append((f"{plage}.{octets[2]}.{octets[3]+1}", f"{plage}.{octets[2]}.{octets[3]+2}"))
            if octets[3] < 249:
                octets[3] += 4
            else:
                octets[2] += 1
                octets[3] = 0
        return subnet_addresses

    
    except (IndexError, ValueError):
        return "Invalid format"

ip = "10.0.0.0/16"
subnet = create_subnets(ip, 100)
print("subnet:", subnet)