#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse, urlencode

#-------------------------------------------------------------------------------------------#
# Code References:
#  - (parse_url) Python Docs urllib.parse, Date Accessed: Feb 10th, 2021
# https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse
#
#  - (lines 109, 125) Tutorials Point HTTP Requests, Date Accessed: Feb 10th, 2021
# https://www.tutorialspoint.com/http/http_requests.htm#:~:text=An%20HTTP%20client%20sends%20an,end%20of%20the%20header%20fields
#
#  - (line 123) bgporter (Apr 9, 2011), mb21 (Nov 15, 2018), Date Accessed: Feb 10th, 2021
# https://stackoverflow.com/questions/5607551/how-to-urlencode-a-querystring-in-python

#-------------------------------------------------------------------------------------------#
def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return int(data.split()[1])

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return data.split('\r\n\r\n')[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def parse_url(self, url):
        parsedUrl = urlparse(url)
        
        self.host = parsedUrl.hostname
        self.port = parsedUrl.port
        self.path = parsedUrl.path

        if self.port == None:
            self.port = 80
        
        if self.path == '':
            self.path = '/'


    def send_request(self, request):
        self.connect(self.host, self.port)
        self.sendall(request)
        response = self.recvall(self.socket)
        self.close()

        print(response)

        return response

    def GET(self, url, args=None):
        self.parse_url(url)

        request = 'GET %s HTTP/1.1\r\nHost: %s\r\n\r\n' % (self.path, self.host)
 
        response = self.send_request(request)
        
        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        self.parse_url(url)
        body = ''

        if args != None:
            body = urlencode(args)
        
        request = 'POST %s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: %s\r\n\r\n%s' % (self.path, self.host, len(body), body)  

        response = self.send_request(request)
        
        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
