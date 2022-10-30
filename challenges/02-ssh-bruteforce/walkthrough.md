# Guess my credentials

## Preparation

- find the ip of the target with a general scan of the network
	-> scanning the system will only reveal that port 22 for ssh is open

- bruteforcing ssh credentials can be done with "hydra"

- we already know about the user "test" and that the password is somehow related
	-> hydra has flags for common passwords
	-> command would look like this: "hydra -l test -e nsr <MACHINE-IP> ssh"

## Get the flag

Using hydra on the machine with "test" reveals that the password is "tset" (backwards).
Now log into the "test" user.

This account contains no further information but we can have a look at what other accounts exist. Use "getent passwd" or directly look at "/etc/passwd".
User accounts normally start from uid 1000.
Inside /etc/passwd we find the user "usesecurepasswords".

The last clue tells us there has to be some kind of wordlist the creator chose the password from.
Most prominent example would be the "rockyou.txt" wordlist (default on Kali Linux under "/usr/share/wordlists/").

With username and a wordlist we can now let hydra do the work again.
"hydra -l usesecurepasswords -P path/to/rockyou.txt -V <MACHINE-IP> ssh" 
As a result we get the password "iloveyou" for user "usesecurepasswords".
Log in over ssh and we will find a presentation-notes.txt file.

