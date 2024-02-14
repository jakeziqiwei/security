import pandas as pd
import requests
import numpy as np
# Code for getting 1000 most visited sites
df = pd.read_csv('tranco-top-1m.csv', header=None)
topsites = df.iloc[0:1000]
topsites.to_csv("step0-topsites.csv", header=False)
topsites.reset_index(inplace=True)


# Code for generating the 1000 random sites
visited_sites = set()

random_sites = df.sample(n=1000)
random_sites.reset_index(inplace=True)
random_sites.to_csv("step0-randomsample.csv", header=False)


# Step 1:


headers = {
    "Connection": "keep-alive",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}


def return_tag(row):
    page_name = row.iloc[2]
    http_url = 'http://' + page_name
    https_url = 'https://' + page_name

    http_accessible = False
    https_accesible = False
    try:
        http_request = requests.get(http_url, timeout=.5, headers=headers)
        returned_url = http_request.url
        if 'http' in returned_url and 'https' not in returned_url:
            http_accessible = True
        elif 'https' in returned_url:
            https_accesible = True
    except:
        pass

    try:
        https_request = requests.get(https_url, timeout=.5, headers=headers)
        returned_url = https_request.url
        if 'https' in returned_url:
            https_accesible = True
    except:
        pass
    return [https_accesible and not http_accessible, https_accesible and http_accessible,
            http_accessible and not https_accesible, not https_accesible and not http_accessible]


def map_val_to_str(x):
    if x.HTTPSonly:
        return 'HTTPSonly'
    elif x.both:
        return "both"
    elif x.HTTPonly:
        return "HTTPonly"
    else:
        return "neither"


random_site_bools = pd.DataFrame(
    random_sites.apply(return_tag, axis=1).tolist())
random_site_bools.columns = ['HTTPSonly', 'both', 'HTTPonly', 'neither']

final_random_sites = random_site_bools.apply(
    lambda x: map_val_to_str(x), axis=1)

final_random_sites = pd.concat([random_sites[1], final_random_sites], axis=1)
final_random_sites.columns = ['url', 'Reachability']
final_random_sites.to_csv("step1-randomsample.csv", header=False)
print(final_random_sites.value_counts())


topsite_bools = pd.DataFrame(topsites.apply(return_tag, axis=1).tolist())
topsite_bools.columns = ['HTTPSonly', 'both', 'HTTPonly', 'neither']

final_top_sites = topsite_bools.apply(lambda x: map_val_to_str(x), axis=1)

final_top_sites = pd.concat([topsites[1], final_top_sites], axis=1)
final_top_sites.columns = ['url', 'Reachability']
final_top_sites.to_csv("step1-topsites.csv", header=False)
print(final_top_sites.value_counts())
