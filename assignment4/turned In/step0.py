import pandas as pd


def create_tranco_df():
    names = ['ranking', 'domain']
    df = pd.read_csv("./tranco-1m-2024-01-25.csv", names=names)
    topsites = (df.head(1000))
    df2 = df[1000:]
    othersites = df2[df2['ranking'] % 1000 == 0]
    topsites.to_csv('step0-topsites.csv', index=None, header=False)
    othersites.to_csv('step0-othersites.csv', index=None, header=False)

    return
