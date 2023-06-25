# cloudflare-dyndns
Basic Python-based dynamic DNS client for Cloudflare.

## How-to
The script expects a mandatory positional argument to specify the configuration file:
```
╰─ ./dyndns-client.py cloudflare.config 
Updating dyndns.example.com with ip: 111.111.111.111 (result: True)
```

## Files
### cloudflare.config
This file contains the information to run the client. (to-do: use scoped tokens)
The first steps is to fill the cloudflare section with your credentials and zone_id
```
# Information for the cloudflare section is available on
# your Cloudflare dashboard, in the API section
[cloudflare]
zone_id = ZONE_ID
email = your@email.com
global_token = GLOBAL_API_TOKEN

# For convenience, you can use the dns-query.py
# script to fill this section.
[record]
record_id = RECORD_ID
record_name = RECORD_NAME
# proxied tells Cloudflare to hide your IP (true) or not (false)
proxied = true         
# TTL value of 1 = automatic
ttl = 1                       
```

### dns-query.py
Support script to help building the configuration file. It uses the credentials in the configuration file to list records in the zone and allows to select the DDNS record of your choice.

### dyndns-client.py
The DDNS client. Expects the path to the config file as a mandatory positional argument.