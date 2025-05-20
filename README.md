# CRACKNET
A simulation tool to demonstrate Denial of Service (DoS) and ARP Spoofing along with a few interesting decryption techniques.
## Features
1. Localhost web app to trigger attacks
2.	DoS attack on a vulnerable server
3.	ARP Spoofing to intercept traffic between two victims
4.	Decryption Interface:
  - Caesar cipher
  - K-letter (wraparound) cipher
  - XOR-based encryption
  - Base64 decryption
  - RSA decryption (with or without private key)

5.	Simple Interface with start/stop control
## Installation
1.	Clone the repository
2.	git clone https://github.com/DeepDiver36/CrackNet.git
cd CrackNet
3.	Install Dependencies pip install -r requirements.txt
## Network Requirements
•	ARP Spoofing: The attacker and the victim must be on the same local network.
•	DoS Attack: Can target devices on different networks, but this requires hosting a public server - for simplicity, it's recommended to keep the target on the same network.
•	Running the App
1.	Run the python script : python app.py
2.	Open your browser and go to: http://localhost:5000
3.	Use Interface to start any of the two attacks:

-For DoS Inputs:
1.	IP Address of the target server (for our demonstration purpose we used the Apache Web server running on Metasploitable2 Virtual Machine)
2.	Port Number (for our demonstration port number 80)
3.	Rate Limit (0 is preferred if want to instantly make the server go down)
4.	Data Size (25000 suggested)
5.	Threads (1000 suggested)
6.	Click the launch attack button
7.	To stop click the stop button

   
-For ARP Spoofing Inputs:
1.	Victim 1 IP address
2.	Victim 2 IP address (For our demonstration these two were communicating via netcat)
3.	Network Interface
4.	Click the Start ARP Spoofing button , it will open a new tab.
5.	To stop the attack click on Stop ARP Spoofing button.

- For Decryption Panel
1. Click the Button
2. Select the desired Cipher
3. Give the encrypted input and required keys if any
4. Get the decrypted output

