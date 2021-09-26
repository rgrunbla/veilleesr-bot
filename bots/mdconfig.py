
from tweepy.streaming import urllib3
from os import path

def get_mdconfig(url):
    pm = urllib3.PoolManager()
    data = pm.request("GET", url, preload_content=False)

    botconfig = data.read().decode('utf-8').splitlines()
    config = {}
    tweets = []
    datamd = []
    l = []
    for bc in botconfig:
        if bc == "# Config": l = config
        elif bc == "# VeilleESR": l = tweets
        elif bc == "# DataESR": l = datamd
        elif len(bc) > 0:
            if (bc[0] == '-') :
                kv = bc[2:].split(":")
                config[kv[0]]=kv[1]
            else: l.append(bc)

    datatweets = []
    for dm in datamd:
        datatweets += get_datamd(dm)

    return({'config':config, 'tweets':tweets, 'datatweets':datatweets})

def get_datamd(url):
    pm = urllib3.PoolManager()
    data = pm.request("GET", url, preload_content=False)
    datamd = data.read().decode('utf-8').splitlines()

    twtexte = "#DataESR"
    twalt = ""
    twurl = ""

    datatweets = []
    for dm in datamd:
        dm = dm.strip(" ")
        if len(dm) > 0:
            if dm[0:9] == "- twtexte": twtexte = dm[10:].strip(" ")
            if dm[0:7] == "- twalt": twalt = dm[8:].strip(" ")
            if dm[0:7] == "- twurl": twurl = dm[8:].strip(" <>")
            if dm[0] == "#": dttext = twtexte + '\n' + dm.lstrip('# ')
            if dm[0] == "!":
                dtimgurl = dm.lstrip("![](").rstrip(")<!- ->")
                dtimgurl = path.dirname(url) + "/" + dtimgurl

                datatweets.append({'text':dttext,'imgurl':dtimgurl, 'alt':twalt, 'url':twurl})

    return(datatweets)


def main():
    print(get_mdconfig("https://github.com/cpesr/veilleesr-bot/raw/master/botconfig.md"))

if __name__ == "__main__":
    main()