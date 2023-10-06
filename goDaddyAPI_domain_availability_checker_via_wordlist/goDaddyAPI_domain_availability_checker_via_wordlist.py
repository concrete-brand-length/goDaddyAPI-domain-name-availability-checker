import time
import requests
import webbrowser 
import csv
from random import randint

# godaddy API credentials for authentication
api_key = "" # Sign-in to GoDaddy developer portal, create API key, and add 
api_secret = "" # Sign-in to GoDaddy developer portal, create API secret, and add. 
req_headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "accept": "application/json"
}


# Read data from a file
def read_file(file, additional_text):
    list = []
    with open(file) as file:
        element = file.readline().rstrip("\n").lower()
        while element != "":
            list.append(additional_text + element)
            element = file.readline().rstrip("\n").lower()
    return list


# Get the number of words to appear in the domain name and handle potential user input exceptions
def get_number_names_in_domain_name():
    while True:
        try:
            number_of_words_per_name = int(input("\nHow many words would you like in the domain name: "))
            break
        except Exception:
            print("Please only enter a number!\n")
    return number_of_words_per_name


# Get the separator to be used be names in the domain name and handle potential user input errors
def get_domain_name_word_separator():
    while True:
        separator_between_words = input("\nWhat separator would you like to use between words (Enter -, . or press enter to add blank space): ")
        if separator_between_words not in ["-", ".",""]:
            print("Please only enter -, ., or press enter for a blank space only\n")
        else:
            break
    return separator_between_words


# Get the desired top-level domain from the user and handle potential input errors by the user
# List of TLD's obtained from ICANN, however, this may need to be updated if certain desired TLD's are not present
def get_top_level_domain(TLD_file):
    TLD_list = read_file(TLD_file, ".")
    while True:
        print("\nDomain to be checked (Enter a ? if you want to see a Wikipedia resource for help)")
        desired_domain = input("What domain would you like to check for (.com, .net, .co.uk): ")
        if desired_domain == "?":
            webbrowser.open("https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains")
        elif desired_domain not in TLD_list:
            print("\nPlease ensure you enter a suitable domain\n")
        else:
            break
    return desired_domain
        

# Generate domains to check
def generate_domain_name_List(names_file, TLD_file):
    domain_name_list = read_file(names_file, "")
    number_of_words_in_domain_name = get_number_names_in_domain_name()
    domain_name_word_separator = get_domain_name_word_separator()
    top_level_domain = get_top_level_domain(TLD_file)
    
    generated_domains = []

    while len(generated_domains) < (len(domain_name_list) ** number_of_words_in_domain_name):
        generated_domain = ""
        for count in range(number_of_words_in_domain_name):
            generated_domain = generated_domain + domain_name_list[randint(0, (len(domain_name_list) - 1))] + domain_name_word_separator
        
        # Corrects appending of a separator after the last word in the domain name
        if generated_domain[-1] == "":
            generated_domain = generated_domain[0: -1] + top_level_domain
        else:
            generated_domain = generated_domain + top_level_domain
        
        # Only appends generated domains that are not in the list
        if generated_domain not in generated_domains:
            generated_domains.append(generated_domain)
    return generated_domains


# assemble the request url with the given domain
def get_req_url(check_domain):
    return f" https://api.godaddy.com/v1/domains/available?domain={check_domain}"


# Makes the request to GoDaddy API and gets response
def check_domain_available(check_domain):
    print(f"\nChecking availability of domain {check_domain}")
    req_url = get_req_url(check_domain)
    req = requests.get(req_url, headers=req_headers)

    # if request is unsuccessful, notifiy the user and stop
    if req.status_code != 200:
        print(f"Could not get availability state of domain {check_domain}")
        print(req.status_code)
        return
    
    # Checks availablity from response json object
    response = req.json()
    if response["available"] == True:
        print("Domain is available")
        write_to_file(response, check_domain)
    elif response["available"] == False:
        print("Domain is not available")
    
# Write an available domain a file
def write_to_file(content, check_domain):
    with open("./availableAddresses.csv", "a") as file:
        theFile = csv.writer(file, dialect="excel")
        theFile.writerow([time.strftime('%d/%m/%Y'), time.strftime('%H:%M'), check_domain, "£{:.2f}".format((content["price"] / (10 ** 6)) * 0.85)])


def main():
    names_file = "./names.txt"
    TLD_file = "./data.iana.org_TLD_tlds-alpha-by-domain.txt"
    domains = generate_domain_name_List(names_file, TLD_file)
    counter = 1

    # Loops through list to check each generated domains availability
    # time.sleep used to account for Godaddy's API limit on requests
    while counter < len(domains):
        if counter % 60 == 0:
            time.sleep(60)
        check_domain_available(domains[counter - 1])
        counter += 1
    
main()