#!/usr/local/bin/python3.3
#
#
# This code was modeled loosley after:
#  https://github.com/balloob/home-assistant/blob/master/homeassistant/components/device_tracker/ddwrt.py
# And I plan to port it to homeassistant sometime
#
# This can be tested with this address:  http://190.53.26.252/update_clients.asp
#

import re
import requests
import yaml

stream = open('config.yaml', 'r') 
config = yaml.load(stream)
stream.close();

def get_data(url):
    try:
        response = requests.get(
            url,
            auth=(config['router_user'],config['router_password']),
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
        print("Invalid response from asus: %s", response)

def client_connected(host):
    """Check of host is connected"""
    #f = open('update_clients.out', 'r')
    #data = f.readline()
    #f.close();
    url = 'http://{}/update_clients.asp'.format(config['router_host'])
    data = get_data(url)
    data.strip().strip("client_list_array = '").strip("';")
    elements = data.split(',')

    aregex = re.compile(r'<[0-9]+>([^>]*)>([^>]*)>([^>]*)>')

    for item in elements:
        for name, ip, mac in aregex.findall(item):
            #print("name="+name+" ip="+ip+" mac="+mac)
            if host == name:
                return True

    return False

print(client_connected("EV1016HDX"))

