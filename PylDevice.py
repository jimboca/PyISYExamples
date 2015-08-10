#
# PylDevice
#
# Generice class for a Pylink device
#
import requests
from requests.auth import HTTPDigestAuth
import re
#import PylDevice.camera.foscam1

# TODO: This should be configurable, and come from the web.py object
this_host = "192.168.1.76"
this_port = "8080"

class PylDevice(object):

    def __init__(self,device,isy,sched):
        self.name     = device['name']
        self.ip       = device['ip']
        self.port     = device['port']
        self.type     = device['type']
        self.model    = device['model']
        self.user     = device['user']
        self.password = device['password']
        self.isy      = isy
        self.sched    = sched
        self.monitor_job = False
        print("PylDevice:init: " + self.name)
        self.setup()

    #http://192.168.1.110:8080/set_alarm.cgi?motion_armed=1&http=1&http_url=http://192.168.1.76:8080/device/alarm
    def setup(self):
        # TODO: Check self.isy.var motion exists
        if self.type == 'camera':
            # TODO: We should set by calling monitor.  But then we don't have a monitor running...
            self.setvar('motion',0);
            payload = {
                'motion_armed' : '1',
                'http': '1',
                'http_url': 'http://192.168.1.76:8080/setvar/motion/1'
            }
            self.get_data("set_alarm.cgi",payload)

    def get_name(self):
        return self.name

    def get_data(self,path,payload):
        url = "http://{}:{}/{}".format(self.ip,self.port,path)
        print("get_data: " + url)
        auth = HTTPDigestAuth(self.user,self.password)
        #auth = (self.user,self.password)
        try:
            response = requests.get(
                url,
                auth=auth,
                params=payload,
                timeout=10
            )
        except requests.exceptions.Timeout:
            print("Connection to the device timed out")
            return
        print("get_data:sent: " + response.url)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 400:
            print("Bad request from device %s: %s", self.name, response.text)
        elif response.status_code == 401:
            # Authentication error
            print(
                "Failed to authenticate, "
                "please check your username and password")
            return
        else:
            print("Invalid response from device: %s", response)

    def setvar(self,name,value):
        print("PylDevice:setvar: " + self.name + " name=" + name + " value="+ str(value))
        # TODO: Catch error
        var = self.isy.variables[2]['s.Pyl.' + self.name + "." + name]
        var.val = value
        if name == "motion":
            if int(value) == 0:
                print("Stopping monitor")
                if self.monitor_job is not False:
                    self.monitor_job.remove()
                    self.monitor_job = False
            else:
                # TODO: Need multiple monitors based on name
                print("Starting monitor")
                self.monitor_job = self.sched.add_job(self.monitor, 'interval', seconds=10, args=[name,value])

    #alarm_regex = re.compile(r'var\s+(.*)=(.*);')
    def monitor(self,name,value):
        print("PylDevice:monitor: "+ self.name + " name=" + name + " value="+ str(value))
        data = self.get_data("get_status.cgi",{})
        #sprint("PylDevice:monitor: data=" + data)
        for item in data.splitlines():
            varl = item.replace('var ','').strip(';').split('=')
            if varl[0] == 'alarm_status':
                print('PylDevice:monitor: ' + varl[0] + '=' + varl[1])
                if str(varl[1]) == '0':
                    self.setvar(name,0)
