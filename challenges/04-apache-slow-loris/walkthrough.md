# Slow Service

## Preparation

- scan the network with nmap "<NETWORK-IP>/24"
	-> will reveal 2 additional open ports (except ssh 22)
	-> webservers on ports 80 and 8080

- Have a look at the webservers we found



## Getting the flag

The website on port 8080 obviously shows the flag if we meet some condition.
The website on port 80 tells us some basic information about Denial of Service attacks and makes sure to let us know it is safe against them.
Next step we should put that to the test.
The picture of the animal has Slow Loris as alternative text. 
Lets try to search for denial of service in combination with slow loris.

We can find some implementations of a slow loris attack script written in Python 2.
The script opens a lot of parallel connections to the specified server and sends incomplete HTTP requests in order to keep the connections alive.

After starting the script we can see that the server is struggling to show the page for a new connection in the browser.
Checking the flag service on port 8080 will reveal the flag after it fails to establish a connection to port 80.
