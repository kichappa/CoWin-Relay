import requests, json, datetime
from bs4 import BeautifulSoup

def cowin_get(district_id, date, session, proxy):
    if proxy=="":
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"
        response = session.get(URL.format(district_id, date), headers={
                        "accept": "application/json",
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
                    })
        return response
    else:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"
        response = session.get(URL.format(district_id, date), headers={
                        "accept": "application/json",
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
                    }, proxies={
                        "http": "http://"+proxy,
                        "https": "https://"+proxy
                    })
        return response

proxies=[]

while True:
    with open("proxy.json", 'r') as f:
        proxies=json.load(f)
        proxies=proxies['proxy']
        f.close()

    # print("0 Proxies={}".format(proxies))
    res = requests.get('https://free-proxy-list.net/anonymous-proxy.html', headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(res.text,"lxml")

    for items in soup.select("#proxylisttable tbody tr"):
        proxy = ':'.join([item.text for item in items.select("td")[:2]])
        try:
            print("Attempting proxy, {}{}".format(proxy, " "*20))
            t = cowin_get(307, "{}-{}-{}".format(datetime.date.today().day, datetime.date.today().month, datetime.date.today().year), requests, proxy)
            print(t.status_code)
            if t.status_code == requests.codes.ok:
                print("New proxy, {}{}".format(proxy, " "*20))
                if proxy not in proxies:
                    proxies.append(proxy)
                # print("Proxies={}".format(proxies))
                
                f=open("proxy.json", 'w')
                json.dump({"proxy": proxies}, f, indent=2)
                f.close()
            else:
                print("Not working...{}\n".format(" "*20))
        except Exception as e:
            # pass
            print("Connection error")
            # print(e)

