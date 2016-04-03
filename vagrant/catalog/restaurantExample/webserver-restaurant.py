from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
import re

# SQL extraction

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



# Preparing the webserver
# 

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body><h1>Hello! Welcome to the Restaurant Database</h1>"
                message += "<a href='restaurant/new'><h1>Make New Restaurant</h1></a>"
                restaurant_names = session.query(Restaurant).order_by('name')
                for i,names in enumerate(restaurant_names):
                    message += "<h2>"+names.name+"</h2>"
                    message += "<ul>"
                    message += "<li><a href='/restaurant/%s/edit'>Edit</a></li>" % i
                    message += "<li><a href='/restaurant/%s/delete'>Delete</a></li>" % i
                    message += "</ul>"

                message += "</body></html>"
                self.wfile.write(message)
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_names = session.query(Restaurant).order_by('name')
                message = ""
                message += "<html><body><h1>Make a new Restaurant</h1>"
                message += "<form method='POST' enctype='multipart/form-data' action='new'><h2>Insert name</h2><input name='message' type='text'><input type='submit' value='Create'></form>"
                message += "</body></html>"
                self.wfile.write(message)
                return

            # Edit
            if re.findall(r'(restaurant/\d+\/edit)',self.path):
                index = re.findall(r'restaurant/(\d+)\/edit',self.path)[0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_names = session.query(Restaurant).order_by('name')
                message = ""
                message += "<html><body><h1>%s</h1>" % restaurant_names[int(index)].name
                message += "<form method='POST' enctype='multipart/form-data' action='edit'><h2>Insert new name</h2><input name='message' type='text'><input type='submit' value='Edit'></form>"
                message += "</body></html>"
                self.wfile.write(message)
                return

            # Delete
            if re.findall(r'(restaurant/\d+\/delete)',self.path):
                index = re.findall(r'restaurant/(\d+)\/delete',self.path)[0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_names = session.query(Restaurant).order_by('name')
                message = ""
                message += "<html><body><h1>Are you sure you want to delete %s ?</h1>" % restaurant_names[int(index)].name
                message += "<form method='POST' enctype='multipart/form-data' action='delete'><input type='submit' value='Delete'></form>"
                message += "</body></html>"
                self.wfile.write(message)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            # self.send_response(301)
            # self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

            if self.path.endswith("/new"):
                restaurant_new = Restaurant(name = messagecontent[0])
                session.add(restaurant_new)
                session.commit()

            if self.path.endswith("/edit"):
                restaurant_names = session.query(Restaurant).order_by('name')
                var= re.findall(r'restaurant/(\d+)\/edit',self.path)
                var= int(var[0])
                restaurant_names[var].name = messagecontent[0]
                session.commit()

            if self.path.endswith("/delete"):
                restaurant_names = session.query(Restaurant).order_by('name')
                var= re.findall(r'restaurant/(\d+)\/delete',self.path)
                var= int(var[0])
                delete_element = restaurant_names[var]
                session.delete(delete_element)
                session.commit()

            output = ""

            output +=  "<html><body>"
            output += " <h2><a href='/restaurant'>Go back</a>?</h2>"

            output += "</html></body>"

            self.wfile.write(output)

        except:
            pass


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webServerHandler)
		print "Web Server running on port %s"  % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()

if __name__ == '__main__':
	main()
