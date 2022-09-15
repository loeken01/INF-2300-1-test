# Assignment 1: The HTTP Server

HTTP requests and responses share a similar structure:
1. A start-line describing the requests to be implemented, or its status of whether successful or a failure. This start-line is always a single line.

2. An optional set of HTTP headers specifying the request, or describing the body included in the message.

3. A blank line indicating all meta-information for the request has been sent.

4. An optional body containing data associated with the request (like content of an HTML form), or the document associated with a response. The presence of the body and its size is specified by the start-line and HTTP headers.

# GET
GET indicates that a resource should be fetched

# POST 
POST indicates that data is pushed to the server (creating or modifying a resource, or generating a temporary document to send back)

# Start line
The start in a HTTP request contains three elements. 

The first element is an HTTP method like GET,PUT or POST, that describes the action to be performed.

The second element is the request target, which usually is a URL or a path of the protocol.

The third element is the HTTP version, which defines the structure of the remaining message, acting as an indicator of the expected version to use for the response.

# HEADERS
HTTP headers from a request follow the same basic structure of an HTTP header: a case-insesitive string followed by a colon ":" and a value whose structure depends upon the header. The whole header, including the value, consist of one single line, which can be quite long.

# BODY
Bodies can be boardly divided into two categories:
The first one being single-resouce bodies, consisting of one single file, defined by the two headers: content-type and content-length

The second one is the multiple-resource bodies, consisting of a multipart body, each containing a different bit of information.

# API NOTES
