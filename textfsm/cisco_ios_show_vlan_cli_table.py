#! /usr/bin/env python3

import clitable
from getpass import getpass
from netmiko import ConnectHandler

# Login info
username = input('Enter username: ')
password = getpass('Enter password: ')

index_file = 'index'
template_dir = '/Users/satish.kumar/PycharmProjects/ntc-ansible/ntc-templates/templates/'


if __name__ == "__main__":

    with open('host_file') as f:
        device_list = f.read().splitlines()

    for device in device_list:
        host = device
        platform = 'cisco_ios'
        command = 'show version'

        device = ConnectHandler(
                    device_type=platform,
                    ip=host,
                    username=username,
                    password=password
                    )

        raw_text = device.send_command(command)

        cli_table = clitable.CliTable(index_file, template_dir)

        # command = 'show vlan'
        # platform = 'cisco_nxos'

        # keys map directly back to column headers in the index file (see previous slide)
        attrs = {'Command': command, 'Platform': platform}

        # rawtxt is the show output as a string; could be from a file or from device in real-time
        cli_table.ParseCmd(raw_text, attrs)

        print(cli_table)

