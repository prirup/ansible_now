#! /usr/bin/env python

import json
import textfsm
from getpass import getpass
from netmiko import ConnectHandler

# Login info
username = input('Enter username: ')
password = getpass('Enter password: ')

TEMPLATES_PATH = "/Users/satish.kumar/PycharmProjects/ntc-ansible/ntc-templates/templates/"

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
        # print("RAW RESPONSE:")
        # print(raw_text)
        # print("-" * 10)

        template = TEMPLATES_PATH + 'cisco_ios_show_version.template'
        table = textfsm.TextFSM(open(template))

        # print("-" * 10)
        # print("ALL HEADER (KEYS) from TextFSM Values:")
        # print(table.header)

        # this actually parses the data
        data = table.ParseText(raw_text)
        # print("THIS IS HOW TEXTFSM PARSES DATA (LIST OF LISTS)")
        # print(json.dumps(data, indent=4))
        # print("-" * 10)


        # this step is optional, but it cleans up the final object from a list of lists to a list of dictionaries
        final_list = []
        for entry in data:
            temp_dict = {}
            for index, value in enumerate(entry):
                temp_dict[table.header[index].lower()] = value
            final_list.append(temp_dict)

        # print("FINAL CONVERTED/PARSED OBJECT:")
        print(json.dumps(final_list, indent=4))

