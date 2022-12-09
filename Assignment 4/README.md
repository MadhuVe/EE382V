# Bitcoin 4 Wi-Fi
Pay for wi-fi with Bitcoin! Users can send Bitcoin to a wallet and then wi-fi from a Raspberry Pi will become available 
for a set amount of time for the user. 

* Abigail Francis
* Madhumitha Venkataraman
* Leilani Horlander-Cruz

Future improvements:
* Time wi-fi is available will be proportional to amount of Bitcoin received
* User interface to provide users with feedback on time left, wi-fi availability, etc.
* Use transaction ID as the wi-fi password
* Interface with Lightning Network
* Host Lightning/Bitcoin node on Raspberry Pi

How to setup demo:
* Set up Raspberry Pi with latest Raspbian OS
* Enable SSH on the Raspberry Pi
* Set up Raspberry Pi as a wi-fi access point using Network Manager[1]
* Set up SSH keypairs and SCP the public key to the Raspberry Pi[4]
* Update test.sh to reflect your path for transaction.txt, Raspberry Pi IP address, and Raspberry Pi password
* Add content from bitcoin.conf to your own configuration, and change the path to where your test.sh is located
* Set up your Bitcoin wallet if you haven't already

How to use demo:
* Send funds to wallet on host machine
* Script will trigger
* Wait for wi-fi to appear on mobile device
* Connect!

Reference links:
1. https://www.tomshardware.com/how-to/raspberry-pi-access-point 
2. https://blog.ruanbekker.com/blog/2021/08/04/how-to-specify-wallet-name-in-bitcoin-core-walletnotify/
3. https://www.cyberciti.biz/faq/unix-linux-execute-command-using-ssh/
4. https://www.ssh.com/academy/ssh/keygen
5. https://www.atlantic.net/dedicated-server-hosting/how-to-pass-password-to-scp-command-in-linux/