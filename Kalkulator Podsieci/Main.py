from subprocess import check_output
import math
import sys
def main_calculator():
    if len(sys.argv) == 0:  #ile jest stringow
        address = get_computer()
    else:
        address = sys.argv[1]
    if not correctness(address):
        return

    print(address)
    net_address = get_net_address(address)
    print(f'Adress sieci binary: {net_address["bin"]}')
    print(f'Adress sieci decimal: {net_address["dec"]}')

    net_class = get_net_class(net_address["bin"])
    print(f'Klasa sieci: {net_class}')

    mask_short = int(address.split('/')[1])
    net_mask = get_net_mask(mask_short)
    print(f'Maska sieci binary: {net_mask["bin"]}')
    print(f'Maska siecidecimal: {net_mask["dec"]}')

    broadcast_address = get_broadcast_address(address)
    print(f'Adres Broadcast binary: {broadcast_address["bin"]}')
    print(f'Adres Broadcast decimal: {broadcast_address["dec"]}')

    min_host = get_min_host(net_address["dec"], mask_short)
    print(f'Min host adres binary: {min_host["bin"]}')
    print(f'Min host adres decimal: {min_host["dec"]}')

    max_host = get_max_host(broadcast_address["dec"])
    print(f'Max host adres binary: {max_host["bin"]}')
    print(f'Max host adres decimal: {max_host["dec"]}')

    hosts_number = get_hosts_number(net_mask['bin'])
    print(f'Maaksymalna ilosc hostow: {hosts_number}')

    plik = open('plik.json', 'w')
    plik.write(f'Adress sieci binary: {net_address["bin"]}\n'f'Adress sieci binary: {net_address["dec"]}\n'f'Klasa sieci: {net_class}\n'f'Maska sieci binary: {net_mask["bin"]}\n'f'Maska sieci binary: {net_mask["dec"]}\n'
               f'Adres Broadcast binary: {broadcast_address["bin"]}\n'f'Adres Broadcast binary: {broadcast_address["dec"]}\n'f'Min host adres binary: {min_host["bin"]}\n'f'Min host adres binary: {min_host["dec"]}\n'
               f'Max host adres binary: {max_host["bin"]}\n'f'Max host adres binary: {max_host["dec"]}\n'f'Maaksymalna ilosc hostow: {hosts_number}' )
    plik.close()

def get_computer():
    cmd = 'ipconfig'
    xml_text = check_output(cmd)
    x = str(xml_text)
    start= x.find("IPv4 Address. . . . . . . . . . . : ") + 36
    a=1
    b=1
    while a == 1:
        first_ip = x[start:start+11]
        if first_ip.find('r') == 1:
            first_ip = x[start:start + 15-b]
            b=b+1
        else:
            a=0
    start = x.find("Subnet Mask . . . . . . . . . . . :") + 36
    first_mask = x[start:start + 14]
    mask_bin = [dec2binary(int(part), 8) for part in first_mask.split('.')]
    mask_short = '.'.join(mask_bin).count('1')  #ilosc wystapien 1
    print(mask_short)
    return{'a': f'{first_ip}/{mask_short}',
            'b': mask_bin}
def dec2binary(number,length):
    queue = []
    while number != 0:
        queue.insert(0, number % 2) #wyperlnia 0 do konca
        number = number // 2  # dzielenie bez reszty
    return f'{"".join(str(i) for i in queue):0>{length}}' # string do ktroego włacza sie zmienne, wypelniam zerami to length
def correctness(address):
    ip = address.split('/')
    correct = True
    ip_parts = ip[0].split('.')
    for part in ip_parts:
        if not part.isnumeric():
            print('Addres is not correct')
            correct = False
        else:
            if not (int(part) >= 0 and int(part) <= 255):
                print('wrong range')
                correct = False
    if len(ip_parts) != 4:
        print('to many o to low part')
        correct = False
    if int(ip[1]) < 0 or int(ip[1]) > 32:
        print('Mask havet to between 0 and 32')
        correct = False
    return correct
def get_net_address(address):
    ip_dec_list = [int(part) for part in address.split('/')[0].split('.')]
    mask_short = int(address.split('/')[1])
    net_bytes = mask_short % 8 #ile dla sieci ile dla hosta
    octet_number = math.ceil(mask_short / 8)
    octet_bin = dec2binary(int(ip_dec_list[octet_number - 1]), 8) #od pewnego momentu siec lub host "3"
    octet_net_part_bin = f'{octet_bin[0:net_bytes]:0<8}'
    octet_net_part_dec = int(octet_net_part_bin, 2) #zmienia na dziesetny
    net_address = list(ip_dec_list)
    net_address[octet_number-1] = octet_net_part_dec
    for i in range(octet_number, 4):
        net_address[i] = 0
    return {
        'bin': '.'.join([dec2binary(part, 8) for part in net_address]), # kazdy part konczony kropka
        'dec': '.'.join(str(part) for part in net_address)
    }
def get_net_class(net_address_bin):
    first_octet = net_address_bin.split('.')[0]
    if first_octet[0] == '0':
        return 'A'
    elif first_octet[0:2] == '01':
        return 'B'
    elif first_octet[0:3] == '110':
        return 'C'
    elif first_octet[0:4] == '1110':
        return 'D'
    elif first_octet[0:4] == '1111':
        return 'E'
def get_net_mask(net_mask_short):
    mask_bin = f'{net_mask_short * "1":0<32}'
    mask_bin = [f'{mask_bin[0:8]:s}', f'{mask_bin[8:16]:s}',
                f'{mask_bin[16:24]:s}', f'{mask_bin[24:32]:s}']
    mask_dec = [int(part, 2) for part in mask_bin]
    return {
        'bin': '.'.join(mask_bin),
        'dec': '.'.join(str(part) for part in mask_dec)
    }
def get_broadcast_address(address):
    ip_dec_list = [int(part) for part in address.split('/')[0].split('.')]
    mask_short = int(address.split('/')[1])
    net_bytes = mask_short % 8
    octet_number = math.ceil(mask_short / 8)
    octet_bin = dec2binary(int(ip_dec_list[octet_number - 1]), 8)
    octet_net_part_bin = f'{octet_bin[0:net_bytes]:1<8}' #jedynkami wypelniam
    octet_net_part_dec = int(octet_net_part_bin, 2)
    broadcast_address = list(ip_dec_list)
    broadcast_address[octet_number-1] = octet_net_part_dec
    for i in range(octet_number, 4):
        broadcast_address[i] = 255
    return {
        'bin': '.'.join([dec2binary(part, 8) for part in broadcast_address]),
        'dec': '.'.join(str(part) for part in broadcast_address)
    }
def get_min_host(net_address_dec, mask_short):
    net_address_dec = [int(part) for part in net_address_dec.split('.')]
    net_address_dec[3] = net_address_dec[3] + 1
    min = '.'.join(str(part) for part in net_address_dec)
    return {
        'bin': '.'.join([dec2binary(part, 8) for part in net_address_dec]),
        'dec': min
    }
def get_max_host(broadcast_address_dec):
    net_address_dec = [int(part) for part in broadcast_address_dec.split('.')]
    net_address_dec[3] = net_address_dec[3] - 1
    max = '.'.join(str(part) for part in net_address_dec)
    return {
        'bin': '.'.join([dec2binary(part, 8) for part in net_address_dec]),
        'dec': max
    }
def get_hosts_number(mask_bin):
    return 2 ** mask_bin.count('0') - 2


main_calculator()