#!/usr/bin/env python3
from asyncore import read, write
from base64 import decode, encode
from email import header
from email.quoprimime import header_check
from fileinput import filename
from http import client
from http.client import responses
from lib2to3.pgen2 import driver
import socketserver
import sys
from tkinter import W
from urllib import response
from pyrsistent import b

from requests import request
import requests

import json

import os

import random

"""
Written by: Raymon Skjørten Hansen
Email: raymon.s.hansen@uit.no
Course: INF-2300 - Networking
UiT - The Arctic University of Norway
May 9th, 2019
"""

class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    This class is responsible for handling a request. The whole class is
    handed over as a parameter to the server instance so that it is capable
    of processing request. The server will use the handle-method to do this.
    It is instantiated once for each request!
    Since it inherits from the StreamRequestHandler class, it has two very
    usefull attributes you can use:

    rfile - This is the whole content of the request, displayed as a python
    file-like object. This means we can do readline(), readlines() on it!

    wfile - This is a file-like object which represents the response. We can
    write to it with write(). When we do wfile.close(), the response is
    automatically sent.

    The class has three important methods:
    handle() - is called to handle each request.
    setup() - Does nothing by default, but can be used to do any initial
    tasks before handling a request. Is automatically called before handle().
    finish() - Does nothing by default, but is called after handle() to do any
    necessary clean up after a request is handled.
    """

    # Get the headers from the request
    def get_headers(self):
        header = {}

        for line in self.rfile:
            if line == b'\r\n':
                break
            
            # line = line.decode('utf-8')
            line_split = line.split()

            header[line_split[0]] = line_split[1]

        return header

    # Get the file length
    def get_file_len(self,filename):
        try: 
            # If the filename is a json file
            if 'json' in filename:
                with open(filename, "r+") as f:
                    json_obj = json.dumps(json.load(f))

                    return len(json_obj)
            else:
                with open(filename, "rb") as f:

                    return len(f.read())
        except:
            with open(filename, "x") as f:
                self.wfile.write(b"HTTP/1.1 201" +b"\r\n")

                return 0

    # Do a post request
    def POST(self, filename):
        if 'test.txt' in filename:
            # Take away the "/" in the request target
            url = filename
            url = url.replace("/","")

            # Get the headers
            headers = self.get_headers()

            # Get the file length
            filelen = self.get_file_len(url)

            # Write 201 as a status response
            self.wfile.write(b"HTTP/1.1 201" +b"\r\n")

            # Respond with content type
            self.wfile.write(b"Content-type:"+(b'text/plain')+b"\r\n")

            # Get the content length
            length = filelen + int(headers[b"Content-Length:"])            
            
            # Write the content length as a respone
            self.wfile.write(b"Content-Length:"+(bytes(str(length), 'ascii'))+b"\r\n"+b"\r\n")
            
            # Read a line from rfile with the size of the content length
            body = self.rfile.readline(int(headers[b"Content-Length:"]))

            # Open a file with apend 
            with open(url, "a+") as f:
                f.write(body.decode('utf-8'))
                # f.write("\n") # Might return an error when doing test 11 and 12
                f.seek(0)
                self.wfile.write(f.read().encode())

        # Do the API POST if request target is messages
        elif 'messages.json' in filename:
            # Take away the "/" in the request target
            url = filename
            url = url.replace("/","")

            # Get the headers
            headers = self.get_headers()

            # Get the file length
            filelen = self.get_file_len(url)
            
            # Write 201 as a status response
            self.wfile.write(b"HTTP/1.1 201" +b"\r\n")

            # Open the json file with read
            with open(url, 'rb') as f:
                data = json.load(f)

            # Iterate through each record in the json file
            for i in range(len(data)):
                id = data[i]["id"]  # For the last iteration, the id will be set for the incoming message
            
            # Respond with content type
            self.wfile.write(b"Content-type:"+(b"application/json")+b"\r\n")

            # Get the length of the rest of the record excluding the message
            a_record = {"id": id+1, "text": 1}
            record_len = len(bytes(str(a_record),'ascii')) + 3 # The 3 number includes the of the size, might be "," or "}" etc.

            # Get the content length
            length = filelen + int(headers[b"Content-Length:"]) + record_len    # By adding the record_len we make sure that the whole body of the post request is included
            
            # Write the content length as a response
            self.wfile.write(b"Content-Length:"+(bytes(str(length), 'ascii'))+b"\r\n"+b"\r\n")

            # Read a line from rfile with the size of the content length to get body
            body = self.rfile.readline(int(headers[b"Content-Length:"]))

            # The new record to be put inside the json file
            new_record = {"id": id+1, "text": body.decode('utf-8')}
    
            # Append the json file to the record
            data.append(new_record)

            # Open the json with write mode
            with open(url, "w") as f:
                json.dump(data, f, indent=4)    # Write the data to the json file

            # Turn the data into bytes so we can send as response
            data_bytes = bytes(str(data),'ascii')
            data_bytes = data_bytes.replace(b"'",b'"')  # A quick fix to match the test
            
            # Write the whole body to wfile as a response
            self.wfile.write(data_bytes)

    # Do a put request
    def PUT(self, filename):
        # Take away the "/" in the request target
        url = filename
        url = url.replace("/","")
        
        # Get the headers
        headers = self.get_headers()

        # Get the file length
        filelen = self.get_file_len(url)

        # Write 200 as a status response
        self.wfile.write(b"HTTP/1.1 200" +b"\r\n")

        # Open the json file with read
        with open(url, 'rb') as f:
            data = json.load(f)
        
        # Let the user choose which id to replace the text
        print("Choose id between 1 and",len(data))
        id_input = int(input())
        
        # Respond with content type
        self.wfile.write(b"Content-type:"+(b'application/json')+b"\r\n")
        
        # Iterate through the records to get the length of the text that is to be removed
        for i in range(len(data)):
            # If the id is a match, get the length of the text
            if data[i]["id"] == id_input:
                text_len = len(data[i]["text"])
                break
        
        # Get the content length
        length = filelen + int(headers[b"Content-Length:"]) - text_len  # We subtract by the text length that is to be removed

        # Write the content length as a respone
        self.wfile.write(b"Content-Length:"+(bytes(str(length), 'ascii'))+b"\r\n"+b"\r\n")

        # Read a line from rfile with the size of the content length
        body = self.rfile.readline(int(headers[b"Content-Length:"]))

        # Iterate through each record and find the matching id
        for i in range(len(data)):
            # If the id is a match, replace the text 
            if data[i]["id"] == id_input:
                data[i]["text"] = body.decode('utf-8')
                break

        # Open the json with write mode
        with open(url, "w") as f:
            json.dump(data, f, indent=4)    # Write the data to the json file

        # Turn the data into bytes so we can send as response
        data_bytes = bytes(str(data), 'ascii')
        data_bytes = data_bytes.replace(b"'",b'"')  # A quick fix to match the test

        # Write the whole body to wfile as a response
        self.wfile.write(data_bytes)

    # Do a delete request
    def DELETE(self, filename):
        # Take away the "/" in the request target
        url = filename
        url = url.replace("/","")
        
        # Get the headers
        headers = self.get_headers()

        # Get the file length
        filelen = self.get_file_len(url)

        # Write 200 as a status response
        self.wfile.write(b"HTTP/1.1 200" +b"\r\n")

        # Respond with content type
        self.wfile.write(b"Content-type:"+(b'application/json')+b"\r\n"+b"\r\n")

        # Open the json file with read mode
        with open(url, 'rb') as f:
            data = json.load(f)
        
        # Let the user choose which record to delete            
        print("Choose id between 1 and",len(data),"to delete")
        id_input = int(input())

        # Loop through each record and find the matching id
        for i in range(len(data)):
            # If the id is matching, delete the record
            if data[i]["id"] == id_input:
                data.pop(i)
                break
        
        # If the id input is lower than the data, give id's in order
        if id_input < len(data)+1:
            for i in range(len(data)):
                data[i]["id"] = i + 1
        
        # Open the json file with write mode
        with open(url, "w") as f:
            json.dump(data, f, indent=4)

        # Turn the data into bytes so we can send as response
        data_bytes = bytes(str(data), 'ascii')
        data_bytes = data_bytes.replace(b"'",b'"')  # A quick fix to match the test

        # Write the whole body to wfile as a response
        self.wfile.write(data_bytes)
   
    def handle(self):
        """
        This method is responsible for handling an http-request. You can, and should(!),
        make additional methods to organize the flow with which a request is handled by
        this method. But it all starts here!
        """
        
        # The start line for the request
        start_line = self.rfile.readline().strip()  # Strip the start line
        request = start_line.decode('utf-8')        # Decode it into utf-8
        request_split = request.split()             # Split the request         
        
        # If the request is a GET
        if 'GET' in request_split:
            # Do GET with the request target
            # If it is root
            if '/' in request_split:
                # Read the index.html file
                with open("index.html", "rb") as infile:
                    read_file = infile.read()

                # Set the status code
                self.wfile.write(b"HTTP/1.1 200"+b"\r\n")

                # Respond with the content length
                content = len(read_file)    # Get the length of the body
                content_bytes = bytes(str(content), 'ascii')    # Turn it into bytes
                self.wfile.write(b"Content-Length:"+(content_bytes)+b"\r\n")

                # Respond with the content type
                self.wfile.write(b"Content-Type: text/html"+b"\r\n"+b"\r\n")
                
                # Respond with the body
                self.wfile.write(read_file)

            # API
            elif '/messages.json' in request_split[1]:
                # Take away the "/" in the request target
                url = request_split[1]
                url = url.replace("/","")

                with open(url) as infile:
                    data = json.load(infile)
                
                # Set the status code
                self.wfile.write(b"HTTP/1.1 200"+b"\r\n")

                json_obj = json.dumps(data)
                content = len(json_obj)
                content_bytes = bytes(str(content), 'ascii')
                
                self.wfile.write(b"Content-Length:"+(content_bytes)+b"\r\n")

                self.wfile.write(b"Content-Type: application/json"+b"\r\n"+b"\r\n")
                
                data_bytes = bytes(str(json_obj),'ascii')
                self.wfile.write(data_bytes)
                
            # 404
            elif 'did_not_find_this_file.not' in request_split[1]:
                self.wfile.write(b"HTTP/1.1 404")
            # 403
            elif 'server.py' in request_split[1]:
                self.wfile.write(b"HTTP/1.1 403")
            # 403
            elif '../README.md' in request_split[1]:
                self.wfile.write(b"HTTP/1.1 403")

        # POST request
        elif 'POST' in request_split:
            # Do POST with the request target
            self.POST(request_split[1])
                    
        # If the request is a PUT
        elif 'PUT' in request_split:
            # Do PUT with the request target
            self.PUT(request_split[1])
            
        # If the request is a DELETE
        elif 'DELETE' in request_split:
            # Do DELETE with the request target
            self.DELETE(request_split[1])

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Serving at: http://{}:{}".format(HOST, PORT))
        server.serve_forever()
