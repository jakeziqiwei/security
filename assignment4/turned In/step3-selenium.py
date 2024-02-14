import os
import signal
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # Run in headless mode
# Bypass OS security model, necessary for Docker containers
# options.add_argument("--no-sandbox")
# Overcome limited resource problems
# options.add_argument("--disable-dev-shm-usage")


names = ['ranking', 'domain']
df_top = pd.read_csv("step0-topsites.csv", names=names)
df_other = pd.read_csv("step0-othersites.csv", names=names)
df_top_new = pd.DataFrame({"response": []})


def access_web(name):

    http = 'http://' + name
    https = "https://" + name
    https_bool = False
    http_bool = False

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(http)
        time.sleep(5)
        url = driver.current_url
        print(url)
        if 'http' in url and 'https' not in url:
            http_bool = True
        elif 'https' in url:
            https_bool = True
        driver.quit()
    except:
        pass

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(https)
        time.sleep(5)
        url = driver.current_url
        print(url)
        if 'https' in url:
            https_bool = True
        driver.quit()
    except:
        pass

    return [https_bool and not http_bool, https_bool and http_bool,
            http_bool and not https_bool, not https_bool and not http_bool]


response_result = ['HTTPSonly', 'both', 'HTTPonly', 'neither']


def mapStatus(arr):
    for i, res in enumerate(arr):
        if res:
            return (response_result[i])


for i in range(len(df_top)):
    name = df_top.iloc[i, 1]
    print(i, name)
    res = access_web(name)
    new_row = pd.DataFrame([mapStatus(res)],
                           columns=df_top_new.columns)
    # print(new_row)
    df_top_new = pd.concat([df_top_new, new_row], ignore_index=True)

df_top_new = pd.concat([df_top, df_top_new], axis=1)
df_top_new.to_csv('step3-topsites-selenium.csv', index=None, header=False)

# for i in range(len(df_other)):
#     name = df_other.iloc[i, 1]
#     print(i, name)
#     res = access_web(name)
#     new_row = pd.DataFrame([[mapStatus(res[1]), res[0]]],
#                            columns=df_top_new.columns)
#     # print(new_row)
#     df_top_new = pd.concat([df_top_new, new_row], ignore_index=True)

# df_top_new = pd.concat([df_other, df_top_new], axis=1)
# df_top_new.to_csv('step3-othersites-selenium.csv', index=None, header=False)
