import pandas as pd
import requests

names = ['ranking', 'domain']
df_top = pd.read_csv("step0-topsites.csv", names=names)
df_other = pd.read_csv("step0-othersites.csv", names=names)
df_top_new = pd.DataFrame({"response": [], 'status': []})


def access_web(name):
    http = 'http://' + name
    https = "https://" + name
    status = 0
    https_bool = False
    http_bool = False
    try:
        http_request = requests.get(http, timeout=0.5)
        url = http_request.url
        status = http_request.status_code
        if status >= 200 and status <= 299:
            if 'http' in url and 'https' not in url:
                http_bool = True
            elif 'https' in url:
                https_bool = True
    except:
        pass

    try:
        https_request = requests.get(https, timeout=0.5)
        url = https_request.url
        status = https_request.status_code
        if status >= 200 and status <= 299:
            if 'https' in url:
                https_bool = True
    except:
        pass

    return (status, [https_bool and not http_bool, https_bool and http_bool,
            http_bool and not https_bool, not https_bool and not http_bool])


response_result = ['HTTPSonly', 'both', 'HTTPonly', 'neither']


# print(access_web('google.com'))


def mapStatus(arr):
    for i, res in enumerate(arr):
        if res:
            return (response_result[i])


for i in range(len(df_top)):
    name = df_top.iloc[i, 1]
    print(i, name)
    res = access_web(name)
    new_row = pd.DataFrame([[mapStatus(res[1]), res[0]]],
                           columns=df_top_new.columns)
    # print(new_row)
    df_top_new = pd.concat([df_top_new, new_row], ignore_index=True)

df_top_new = pd.concat([df_top, df_top_new], axis=1)
df_top_new.to_csv('step3-topsites-requests.csv', index=None, header=False)


# for i in range(len(df_other)):
#     name = df_other.iloc[i, 1]
#     print(i, name)
#     res = access_web(name)
#     new_row = pd.DataFrame([[mapStatus(res[1]), res[0]]],
#                            columns=df_top_new.columns)
#     # print(new_row)
#     df_top_new = pd.concat([df_top_new, new_row], ignore_index=True)

# df_top_new = pd.concat([df_other, df_top_new], axis=1)
# df_top_new.to_csv('step3-othersites-requests.csv', index=None, header=False)
