#!/usr/bin/python
#

import web

urls = (
    '/device/*(.*)', 'device',
    '/(.*)', 'default'
)

global foo
foo = False

app = web.application(urls, globals())

class default:
    def GET(self, name):
        if not name:
            name = 'World'
        return 'Default, ' + name + '!'

class device:
    def GET(self, command):
        if not command:
            name = 'Notdefined'
        udata = web.input(cname="not_defined",st=0)
        print web.fvars
        dip = web.ctx['ip']
        print('Device: ' + dip + ' command='+ command + ' cname=' + udata.cname + ' st=' + str(udata.st))
        return 'Device: ' + name + ' cname=' + udata.cname + ' st=' + str(udata.st) + '!'

if __name__ == "__main__":
    app.run()
