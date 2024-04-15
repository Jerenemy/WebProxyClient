#!/usr/bin/python3
#
# Wesleyan University
# COMP 332
# Homework 3: Simple multi-threaded web proxy

# Usage:
#   python3 web_proxy.py <proxy_host> <proxy_port> <requested_url>

# Jeremy Zay

# Python modules
import socket
import sys
import threading

# Project modules
import http_constants as const
import http_util
import cache 

class WebProxy():

    def __init__(self, proxy_host, proxy_port):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_backlog = 1
        self.cache_collection = cache.CacheList([])
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.bind((self.proxy_host, self.proxy_port))
            proxy_sock.listen(self.proxy_backlog)
        except OSError as e:
            print ("Unable to open proxy socket: ", e)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)

        # Wait for client connection
        while True:
            print("Waiting for client connection...")
            conn, addr = proxy_sock.accept()
            print ('Client has connected', addr)
            thread = threading.Thread(target = self.serve_content, args = (conn, addr))
            thread.start()

    def serve_content(self, conn, addr):
        
        # print("starting serve_content...")
        # Receive byte request from client
        bin_req = b''
        print("Receiving request from client...")
        while True:
            # print("getting more...")
            more = conn.recv(1024)

            # print(f"{more}")
            if not more:
                break
            bin_req += more
            
            # keeps not being able to receive empty message, so forcing it to end
            if const.END_HEADER.encode('utf-8') in bin_req:
                break
        # print("got bin_req...")
        
        # decode HTTP GET Request
        try:
            str_req = bin_req.decode('utf-8')
            print(str_req)
        except ValueError as e:
            print ("Unable to decode request, not utf-8", e)
            conn.close()
            return 
        # print("decoded bin_req...")
        # print(f"str_req = \n{str_req}]\n\n")
        
        # Extract host and path from HTTP GET Request
        hostname = http_util.get_http_field(str_req, 'Host: ', const.END_LINE)
        
        # account for server sending GET request in HTTP/1.1
        if ' HTTP/1.0' in str_req:
            pathname = http_util.get_http_field(str_req, 'GET ', ' HTTP/1.0')
        elif ' HTTP/1.1' in str_req:
            pathname = http_util.get_http_field(str_req, 'GET ', ' HTTP/1.1')
        else: print("error\n\n")
        
        if hostname == -1 or pathname == -1:
            print ("Cannot determine host")
            conn.close()
            return
        elif pathname[0] != '/':
            [hostname, pathname] = http_util.parse_url(pathname)
        # create HTTP GET Request
        str_req = http_util.create_http_req(hostname, pathname)
        # create url
        url = hostname + pathname
        
        # if already in cache, add 'If-Modified-Since' field to HTTP GET Request
        if self.cache_collection.is_url_in_cache(url):
            str_req = self.cache_collection.create_last_modified_req(str_req, url)

        
        # Open connection to host and send binary request        
        bin_req = str_req.encode('utf-8')
        try:
            web_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            web_sock.connect((hostname, 80))
            print ("Sending request to web server: ", str_req)
            web_sock.sendall(bin_req)
        except OSError as e:
            print ("Unable to open web socket: ", e)
            if web_sock:
                web_sock.close()
            conn.close()
            return

        # Wait for response from web server
        bin_reply = b''
        while True:
            # print("waiting for more reply...")
            more = web_sock.recv(1024)
            # print(f"{more}")
            if not more:
                 break
            bin_reply += more

        print(f"\nProxy received from server (1st 300 chars): \n{bin_reply[:300]}")
        
        # if URL not yet in cache, add to cache, return HTTP response
        # if URL in cache and unmodified since last Request, return cached HTTP response
        # if URL in cache and modified, return HTTP response
        cache_response = self.cache_collection.get_response_and_update_cache(url, bin_reply)
        
        # Send web server response to client
        # print('Proxy received from server (showing 1st 300 bytes): ', bin_reply[:300])
        print('\nProxy sending server msg to client (1st 300 chars): ', cache_response[:300])

        self.cache_collection.print_urls_in_cache()
        # print("sending cache_response to conn...")
        conn.sendall(cache_response)

        # Close connection to client
        conn.close()


def main():

    print (sys.argv, len(sys.argv))

    proxy_host = 'localhost'
    proxy_port = 50007

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])

    web_proxy = WebProxy(proxy_host, proxy_port)

if __name__ == '__main__':

    main()
