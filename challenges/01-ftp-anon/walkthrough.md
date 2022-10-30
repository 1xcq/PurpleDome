# Exam Heist Walkthrough

## Preparation

- scan the network to find the target
	-> "nmap <NETWORK-IP>/24"
	-> a shortcut in this case is "ping target1.local"

- scan the machine to see what services are running 
	-> "nmap <MACHINE-IP> -sV -O" (version and OS scan)
	-> now we know the system is running an vsFTPd server on port 21

- nmap can also gather further information about the running ftp service 
	-> the option "--script ftp-anon" (included in "-A") checks for anonymous access and even enumerates files accessible on the server



## Get the flag

After the scan we know how we havet to authenticate against the server.
Login in with the username anonymous, leave the password empty.
Fetch the exam file and have a look at it.
