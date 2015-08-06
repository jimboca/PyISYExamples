#!/usr/local/bin/python3.3
#

import re
import requests

def get_data(url):
    try:
        response = requests.get(
            url,
            #auth=(username,passwod),
            timeout=4
        )
    except requests.exceptions.Timeout:
        print("Connection to the asus router timed out")
        return
    if response.status_code == 200:
        return response.text
    elif response.status_code == 401:
        # Authentication error
        print(
            "Failed to authenticate, "
            "please check your username and password")
        return
    else:
        print("Invalid response from ddwrt: %s", response)

def client_connected(host):
    """Check of host is connected"""
    #f = open('update_clients.out', 'r')
    #data = f.readline()
    #f.close();
    data = get_data("http://190.53.26.252/update_clients.asp")
    data.strip().strip("client_list_array = '").strip("';")
    elements = data.split(',')
    print(elements)

    aregex = re.compile(r'<[0-9]+>([^>]*)>([^>]*)>([^>]*)>')

    for item in elements:
        for name, ip, mac in aregex.findall(item):
            print("name="+name+" ip="+ip+" mac="+mac)
            if host == name:
                return True

    return False

print(client_connected("EV1016HDX"))

