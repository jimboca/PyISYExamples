#!/usr/bin/python
#

import web

# TODO: This is a dumb way to reference:
urls = (
    '/setvar/*(.*)', 'setvar',
    '/(.*)', 'default'
)
PylRESTObj = False

class PyISYLinkREST(object):
    global PylRESTObj

    def __init__(self,devices):
        global PylRESTObj
        self.app = web.application(urls, globals())
        self.devices = devices
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
        # TODO: Generate error if device does not exist
        device = PylRESTObj.devices.get_device(dip)
        info = 'Device: ' + dip + ' varname='+ varname + ' value=' + str(varvalue)
        PylRESTObj.devices.logger.info(info)
        device.setvar(varname,varvalue)
        return info

#if __name__ == "__main__":
#    #PylREST.run()
