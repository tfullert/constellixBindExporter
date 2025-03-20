import time
import requests
import hashlib
import base64
import hmac
import argparse

# Configure command line parameters for the script
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-p", "--per", type=str, default="50", help="number of domains to return per API call")

args = parser.parse_args()

# Variables used to create token and call 'list domain' API
url         = "https://api.dns.constellix.com/v4/domains?"
apiKey      = "[TODO: API_KEY]"
secretKey   = "[TODO: SECRET_KEY]"
epochTime   = str(round(time.time() * 1000))

# Function for generating signature used in token
def gen_hmac_sha1(key, msg):
    hmac_sha1 = hmac.new(key.encode('utf-8'), msg.encode('utf-8'), hashlib.sha1)
    signature = base64.b64encode(hmac_sha1.digest()).decode('utf-8')
    return signature

# Token generation & pagination variable for 'list domain' API
sig             = gen_hmac_sha1(secretKey, epochTime)
tok             = apiKey + ':' + sig + ':' + epochTime
next_page_url   = ''

while True:
    
    # Response from 'list domain' API includes meta data that is used for navigating pagination of results
    if next_page_url == None:
        # ...No more pages
        break  
    elif next_page_url:
        # ...There's another page
        curr_page_url = next_page_url
    else:
        # ...This is the first page
        curr_page_url = url + f"page=1&perPage=" + args.per

    # Call 'list domains' API
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + tok
    }

    # Process results and get next page for pagination
    print(f"INFO: Getting {curr_page_url}.")
    response        = requests.request("GET", curr_page_url, headers=headers, data=payload)
    domain_list_rsp = response.json()
    domain_id_list  = []
    next_page_url   = domain_list_rsp['meta']['links']['next']
    
    print(f"INFO: Setting next_page_url to {next_page_url}.")

    if domain_list_rsp['data']:

        # Get the id for each domain returned
        for domain in domain_list_rsp['data']:
            domain_id_list.append(domain['id'])
            domain_name = domain['name']
            
            # Call the 'Bind Export' API for each domain id
            url = f"https://api.dns.constellix.com/v4/domains/{domain['id']}/bind"
            
            print(f"INFO: Calling {url}.")
            
            payload = {}
            headers = {
                'Accept': 'text/plain',
                'Authorization': 'Bearer ' + tok
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            
            # Save the payload (BIND formatted file) in a file named <domain_name>.bind
            with open(domain_name + '.bind', 'w') as f:
                f.write(response.text)
                print(f"INFO: Saving BIND formatted file {domain_name}.bind.")

print("INFO: Done!")