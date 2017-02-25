import  cgi
import  webapp2
import  jinja2
import  os
import  datetime
import sys
#sys.path.append('./pdfkit-0.4.1/')
#
#import  pdfkit
import  StringIO

from google.appengine.api import users

jinja_env   =jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(open('index.html').read())

class assignmentbuilder(webapp2.RequestHandler):
    def write(self):
        self.data   ={}
        self.fields =['firstname','lastname','date',\
                        'length','topic','resources']

        for f in self.fields:
            self.data[f]    =self.request.get(f)

        for f in self.fields:
            print f,self.data[f]

    def post(self):
        jinja_env   =jinja2.Environment(\
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
        self.write()
        template    =jinja_env.get_template('TalkForm.html')

        print '*'*55
        print self.data
        print '*'*55
        self.data['name'] = self.data['firstname'].title() + ' ' + self.data['lastname'].title()
        self.data['date'] = datetime.datetime.strptime(self.data['date'],'%Y-%m-%d').strftime('%A %B %d %Y')

        outputtext  =template.render(self.data)
        output = StringIO.StringIO()
        output.write(outputtext)
        self.response.out.write(outputtext)

        #PDF = pdfkit.from_file(output,'out.pdf')
        #pdfkit.from_url('http://google.com',False)
        #self.response.headers['Content-Type'] = 'application/pdf'
        #self.response.headers['Content-Disposition'] = 'attachment; filename=Myfile.pdf'
        #self.response.headers['Content-Transfer-Encoding'] = 'binary'
        #self.response.out.write(PDF.getvalue())

app = webapp2.WSGIApplication(  [('/', MainPage),
                                ('/sign', assignmentbuilder)
                                ],
                                debug=True)

