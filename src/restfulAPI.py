import json
import socketserver
import threading
from time import sleep

from pyrsistent import b
from server import MyTCPHandler as HTTPHandler
from http import HTTPStatus
from http.client import HTTPConnection, BadStatusLine
import os
from random import shuffle



"""
Written by: Raymon Skjørten Hansen
Email: raymon.s.hansen@uit.no
Course: INF-2300 - Networking
UiT - The Arctic University of Norway
May 9th, 2019
"""


RANDOM_TESTING_ORDER = True

HOST = "localhost"
PORT = 54321

with open("server.py", "rb") as infile:
    FORBIDDEN_BODY = infile.read()

with open("messages.json", "rb") as infile:
    test = json.dumps(json.load(infile))
    EXPECTED_BODY = bytes(str(test), 'ascii')

class MockServer(socketserver.TCPServer):
    allow_reuse_address = True


server = MockServer((HOST, PORT), HTTPHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
client = HTTPConnection(HOST, PORT)

def GET():
    """ GET-request to messages returns 'messages.json' """
    client.request("GET", "/messages.json")
    body = client.getresponse().read()
    client.close()

    # Nice prints for debug
    # print("\nEXPECTED_BODY:", EXPECTED_BODY)
    # print("\nBODY         :", body)
    
    return EXPECTED_BODY == body

def POST():
    """ POST-request to messages returns body """
    testfile = "messages.json"
    msg = b'text=Simple test'
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Content-Length": len(msg),
    }

    client.request("POST", testfile, body=msg, headers=headers)
    response_body = client.getresponse().read()
    with open(testfile, "rb") as infile:
        filecontent = bytes(str(json.dumps(json.load(infile))),'ascii')
    client.close()

    # Nice prints for debug
    # print("\n")
    # print("RESPONSE BODY:",response_body,"\n")
    # print("FILECONTENT  :",filecontent,"\n")

    return response_body == filecontent

def PUT():
    """ PUT-request to messages returns body """
    testfile = "messages.json"
    print('Enter message for PUT:')
    x = input()
    msg = bytes(x, 'ascii')
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Content-Length": len(msg),
    }

    client.request("PUT", testfile, body=msg, headers=headers)
    response_body = client.getresponse().read(1000)
    with open(testfile, "rb") as infile:
        filecontent = bytes(str(json.dumps(json.load(infile))),'ascii')
    client.close()

    # Nice prints for debug
    # print("\n")
    # print("RESPONSE BODY:",response_body,"\n")
    # print("FILECONTENT  :",filecontent,"\n")

    return response_body == filecontent

def DELETE():
    """ DELETE-request to messages returns body """
    testfile = "messages.json"

    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
    }

    client.request("DELETE", testfile, headers=headers)

    response_body = client.getresponse().read()
    with open(testfile, "rb") as infile:
        filecontent = bytes(str(json.dumps(json.load(infile))),'ascii')
    client.close()

    # Nice prints for debug
    # print("\n")
    # print("RESPONSE BODY:",response_body,"\n")
    # print("FILECONTENT  :",filecontent,"\n")

    return response_body == filecontent


# Might have to test one function at a time
test_functions = [
    GET,
    POST,
    PUT,
    DELETE,
]


def run_tests(all_tests, random=False):
    passed = 0
    num_tests = len(all_tests)
    skip_rest = False
    for test_function in all_tests:
        if not skip_rest:
            result = test_function()
            if result:
                passed += 1
            else:
                skip_rest = True
            print(("FAIL", "PASS")[result] + "\t" + test_function.__doc__)
        else:
            print("SKIP\t" + test_function.__doc__)
    percent = round((passed / num_tests) * 100, 2)
    print(f"\n{passed} of {num_tests}({percent}%) tests PASSED.\n")
    if passed == num_tests:
        return True
    else:
        return False


def run():
    print("Running tests in sequential order...\n")
    sequential_passed = run_tests(test_functions)
    # We only allow random if all tests pass sequentially

    # TURN ON OR OFF IF NEEDED BUT SEQUENTIAL ORDER IS BETTER FOR NOW
    # if RANDOM_TESTING_ORDER and sequential_passed:
    #     print("Running tests in random order...\n")
    #     shuffle(test_functions)
    #     run_tests(test_functions, True)
    # elif RANDOM_TESTING_ORDER and not sequential_passed:
    #     print("Tests should run in sequential order first.\n")


run()
server.shutdown()