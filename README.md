# goDaddyAPI-domain-name-availability-checkers

## Description
Created to help a friend who wanted to get a business name and domain, but found most of there ideas had already been used. To expedite the naming checking process, one program was created to allow for quick testing of domain name ideas and another was adapted to allow a file of keywords to be used, along with combining with different TLD's. 

## Using the programs locally
1. Activate the virtual environment
``` bash
# Windows
venv\bin\activate

# Linux/Mac OS
source venv\bin\activate
```
2. Ensure dependencies are installed (Install pip if not already installed)
``` bash
# Install requests module
pip install requests
```
3. Go to the GoDaddy developer portal, create an account/sign-in, and create API key (including API secret)
4. Add API key and secret to relevent sections within the code (between lines 5 and 8)
5. Run the program
6. ``` bash
   # Windows
   python goDaddyAPI_domain_availability_checker_via_terminal_input.py
   # or
   python goDaddyAPI_domain_availability_checker_via_wordlist.py

   # MacOS/Linux
   python3 goDaddyAPI_domain_availability_checker_via_terminal_input.py
   # or
   python3 goDaddyAPI_domain_availability_checker_via_wordlist.py
   ````
