#!/usr/bin/python
#

import web

# TODO: This is a dumb way to reference:
urls = (
    '/setvar/*(.*)', 'setvar',
    '/(.*)', 'default'
)
PylRESTApp = web.application(urls, globals())
PylRESTObj = False

class PylREST(object):
    global PylRESTObj

    def __init__(self,devices):
        global PylRESTObj
        self.app = PylRESTApp
        self.devices = devices
        self.byip = {}
        for device in devices:
            self.byip[device.ip] = device
        PylRESTObj = self

    def run(self):
        self.app.run()

class default:

    def GET(self, name):
        if not name:
            name = 'World'
        return 'Default, ' + name + '!'

class setvar:

    def GET(self, path):
        if not path:
            return "varname/value not defined!"
        # TODO: Allow value param to be passed in?
        # TODO: Make sure split only returns 2 objects?
        #udata = web.input(value=None)
        li = path.split("/")
        varname = li[0]
        varvalue = li[1]
        dip = web.ctx['ip']
        print("device: " + dip)
        # TODO: Generate error if device does not exist
        device = PylRESTObj.byip[dip]
        info = 'Device: ' + dip + ' varname='+ varname + ' value=' + str(varvalue)
        print(info)
        device.setvar(varname,varvalue)
        return info

#if __name__ == "__main__":
#    #PylREST.run()
