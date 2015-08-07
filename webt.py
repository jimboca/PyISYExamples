#!/tools/bin/python
#

import web
        
urls = (
    '/camera/*(.*)', 'camera',
    '/(.*)', 'default'
)

app = web.application(urls, globals())

class default:        
    def GET(self, name):
        if not name: 
            name = 'World'
        return 'Default, ' + name + '!'

class camera:        
    def GET(self, name):
        if not name: 
            name = 'Notdefined'
        udata = web.input(cname="not_defined",st=0)
        return 'Camera: ' + name + ' cname=' + udata.cname + ' st=' + str(udata.st) + '!'

if __name__ == "__main__":
    app.run()
