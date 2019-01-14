#! /usr/bin/env python

import json
import textfsm
from getpass import getpass
from netmiko import ConnectHandler

# Login info
# username = 'satish.kumar.adm''
password = getpass('Enter password: ')

TEMPLATES_PATH = "/Users/satish.kumar/PycharmProjects/ntc-ansible/ntc-templates/templates/"

if __name__ == "__main__":

    with open('host_file') as f:
        device_list = f.read().splitlines()

    for device in device_list:
        host = device
        platform = 'cisco_ios'
        command = 'show cdp neighbor'

        device = ConnectHandler(
                    device_type=platform,
                    ip=host,
                    username='satish.kumar.adm',
                    password=password
                    )

        raw_text = device.send_command(command)
        # print("RAW RESPONSE:")
        # print(raw_text)
        # print("-" * 10)

        template = TEMPLATES_PATH + 'cisco_ios_show_cdp_neighbors.template'
        table = textfsm.TextFSM(open(template))

        # print("-" * 10)
        # print("ALL HEADER (KEYS) from TextFSM Values:")
        # print(table.header)

        # this actually parses the data

        data = table.ParseText(raw_text)
        # print("THIS IS HOW TEXTFSM PARSES DATA (LIST OF LISTS)")
        # print(json.dumps(data, indent=4))
        # print("-" * 10)

        print("DeviceName: {}".format(host))
        # print("header: {}".format(table.header))

        # table_list = {i: data[i] for i in range(0, len(data))}
        # dictOfWords = {i: listOfStr[i] for i in range(0, len(listOfStr))}
        print(table_list)

        # this step is optional, but it cleans up the final object from a list of lists to a list of dictionaries
        final_list = []
        for entry in data:
            # print("entry name: {}".format(entry))
            temp_dict = {}
            for index, value in enumerate(entry):
                temp_dict[table.header[index].lower()] = value
            final_list.append(temp_dict)



        #final_list.append(temp_dict)


           #print("hearder"table.header))

        # print("FINAL CONVERTED/PARSED OBJECT:")
        # print("DeviceName is: {}".format(host))

        # temp_dict["deviceName"] = host
        # temp_dict["header"] = table.header
        print(json.dumps(final_list, indent=4))
        # print(table.header)
        # print("++++++++++++++++++++++++++++++++++")
        # print(len(final_list))
