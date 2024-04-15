README - HW3 - Jeremy Zay

FILES INCLUDED:

1. web_proxy.py
2. web_client.py
3. cache.py
4. http_util.py
5. http_constants.py

web_proxy.py: 
- "server" role:
    - listens for connections on host 'localhost' and port 50007
    - opens a socket for client to connect to and accepts client connection
    - accepts the HTTP GET Request from the client
    - extracts URL from HTTP GET Request
    - parses the URL into a valid HTTP/1.0 GET Request
    - if URL stored in cache:
        - creates modified GET Request with added 'If-Modified-Since' field 
- "client" role:
    - connects to the server determined by the URL
    - sends the HTTP/1.0 GET Request to the server
    - receives the HTTP Response
    - if URL not yet in cache, or if URL in cache and modified
        - update cache
        - forward new HTTP response back to client
    - if URL in cache and unmodified since last Request
        - forward cached HTTP response back to client

web_client.py: 
- connects to the socket opened by the web_proxy on host 'localhost' and port 50007
- sends the URL to the web_proxy
- waits for a response back from the web_proxy containing the HTTP Response from the HTTP GET request sent to the server of that URL
- prints the HTTP Response

cache.py:
- contains a Cache class, and a CacheList class
- Cache:
    - stores the URL, the last valid response, and the last modified and date fields.
    - contains operations to perform on a specific cache
- CacheList:
    - contains a list of Cache objects, a new one created whenever a new URL is encountered
    - used to create HTTP request with 'If-Modified-Since' field, and to return cached request, if unmodified 

http_util.py:
- contains useful functions for handling URLs and GET Requests

http_constants.py:
- contains useful constants related to GET Requests


HOW TO RUN:


1. Run web_proxy.py:

Run web_proxy.py using the following command:
    % python3 web_proxy.py

This will open a socket with default host address 'localhost' and default port number 50007. To set a specific host or port, run passing additional arguments:
    % python3 web_proxy.py 'localhost' 50007

You should receive the output:
    '['web_proxy.py'] 1'
and the program pauses.

If you receive the output:
    Unable to open proxy socket:  [Errno 48] Address already in use
then you likely recently closed the connection, and need to wait about a minute before running the program again.


2. Run web_client.py OR use a web browser:

a. Run web_client.py using the following command:
    % python3 web_client.py

This will connect to the socket with default host address 'localhost' and default port number 50007, and send the default url 'info.cern.ch' to the proxy.
To set a specific host, port, or url, run passing additional arguments:
    % python3 web_client.py 'localhost' 50007 'info.cern.ch'

Any url can be requested, as long as it is 'http://', NOT 'https://':
    'http://info.cern.ch'
    'http://info.cern.ch/'
    'http://info.cern.ch/hypertext/WWW/TheProject.html'

If the web_client returns the error:
    'Unable to connect to socket:  [Errno 61] Connection refused'
Be sure that the web_proxy is running and the hosts and ports match.


b. Enable 'Web Proxy (HTTP)' with the same Server and Port as your web_proxy.py (ie 'localhost', 50007) in System Settings > Wi-Fi > Details... > Proxies:

Launch web browser, and enter an 'http://' URL:
    http://info.cern.ch


3. Wait for HTTP Response:

You should get the following output in web_server.py:
    'Client has connected ('127.0.0.1', 50961)'

You should eventually send the Request and receive the Response from the server.
Upon receiving the response, the cache will be updated.
The updated cache will be printed in web_proxy.py

PROBLEMS:

Sometimes the proxy cannot finish accepting the byte request from the client, when waiting for an empty byte msg. I attempted to fix this by having the proxy stop accepting from the server when it encounters the END_HEADER sequence '\r\n\r\n'.

Sometimes the web_proxy gets stuck trying to accept the client connection, and waits there forever. Refreshing the webpage, opening a new webpage, or just waiting may fix this.

Sometimes 'http://example.com' doesn't work.