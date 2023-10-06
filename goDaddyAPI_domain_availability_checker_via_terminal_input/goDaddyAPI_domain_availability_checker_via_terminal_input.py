import time
import requests

# godaddy API credentials for authentication
api_key = "" # Sign-in to GoDaddy developer portal, create API key, and add 
api_secret = "" # Sign-in to GoDaddy developer portal, create API secret, and add. 
req_headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "accept": "application/json"
}

# assemble the request url with the given domain
def get_req_url(check_domain):
    return f" https://api.godaddy.com/v1/domains/available?domain={check_domain}"

def check_domain_available(check_domain):
    print(f"\nChecking availability of domain {check_domain}")
    req_url = get_req_url(check_domain)
    req = requests.get(req_url, headers=req_headers)

    # if request is unsuccessful, notifiy the user and stop
    if req.status_code != 200:
        print(f"\nCould not get availability state of domain {check_domain}")
        print(req.status_code)
        return
    
    # Check if the domain is available
    response = req.json()
    if response["available"] == True:
        with open("./domain_search_results.txt", "a") as file:
            # add repeating values to variables
            message = f"\n{time.strftime('%d-%b-%Y %H:%M')} - Domain {check_domain} is available for purchase\n"
            DETAILS_SECTION = "Details of the response: "
            gbp_price = "\t- Price in GBP: £{:.2f} @ 0.85 GBP to 1 USD".format((response["price"] / (10 ** 6)) * 0.85)
            
            # Print and write to file
            print(message + "\n" + DETAILS_SECTION + "\n")
            file.write(message + "\n" + DETAILS_SECTION + "\n")
            
            # Iterate through json response
            for item in response:
                if item == "period":
                    print(f"\t- {item}: {response[item]} year")
                    file.write(f"\t- {item}: {response[item]} year\n")
                elif item not in ["price", "currency", "definitive"]:
                    print(f"\t- {item}: {response[item]}")
                    file.write(f"\t- {item}: {response[item]}\n")

            
            # Print and write GBP price
            print(gbp_price)
            file.write(gbp_price)
        
            # print and write newline characters for readability
            print("\n")
            file.write("\n")

    else:
        print(f"\n{time.strftime('%d-%b-%Y %H:%M')} - Domain is not available")

print("GoDaddy domain availability checker")

while True:
    # get input of a domain to check
    args = input("\nEnter domain to check (Enter q to quit): ")
    if args == "q":
        exit()
    else:
        check_domain_available(args)

