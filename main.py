import requests, ast, copy, datetime, json, random
from time import sleep

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
   
def print_slots(slots):
    text=""
    offset=len("  Slots:[")
    offset_text=""
    for i in range(offset):
        offset_text+=" "
    i=0
    for slot in slots:
        text+=("\n"+offset_text+slot if i else slot)
        i+=1
    return text

def print_session(session):
    return "\n  Date: {}\n  Available Capacity: {}\n  Type: {}\n  Slots:[{}]".format(session['date'], session['available_capacity'], session['vaccine'], print_slots(session['slots']))

def print_vaccine(vaccines):
    text="\n  Vaccines:["
    offset=len(text)
    offset_text=""
    for i in range(offset):
        offset_text+=" "
    i=0
    for vaccine in vaccines:
        text+= ("\n{}".format(offset_text) if i else "") + "{} - ₹{}".format(vaccine['vaccine'], vaccine['fee'])
    text+="]"
    return text

def print_centres(centres):
    text=""
    for centre in centres:
        print(len(text))
        text+=("\n\n{}: ".format(centre['name']) if len(text) else "{}: ".format(centre['name']))
        if not len(centre['sessions']):
            text+="\nNo slots avaiable"
        else:
            try:
                text+="{}".format(print_vaccine(centre['vaccine_fees']))
            except:
                pass
            for session in centre['sessions']:
                text+="{}".format(print_session(session))
    return text

def available_centres(resp_json):
    centres=[]
    for centre in resp_json['centers']:
        new_centre=copy.deepcopy(centre)
        new_centre['sessions']=[]
        for session in centre['sessions']:
            # print("session capacity={}, type={}, {}".format(session['available_capacity'], type(session['available_capacity']), bool(session['available_capacity'])))
            if bool(session['available_capacity']):
                slot_availabe=True
                new_centre['sessoions'].append(session)
                # print(centre['name'], session, sep="\n")
        if len(new_centre['sessions']):
            centres.append(new_centre)
    return centres

bot_token="1837974035:AAHJ0SCrHgk-F8ByCB5i3hHBXUZzkOT4Lkw"
chat_id="638540040"

def telegram_bot_sendtext(bot_message):
    # bot_token = ''
    # bot_chatID = ''
    with open("token.json", 'r') as f:
        tokens=json.load(f)
        bot_token=tokens['bot_token']
        bot_chatID=str(tokens['bot_chatID'])
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

if __name__=="__main__":
    while True:
        try:
            print("Fetching CoWin API...{}".format(" "*20), end="\r")
            proxies = []
            with open("proxy.json", 'r') as f:
                proxies=json.load(f)
                proxies=proxies['proxy']
                proxies.append("")
            # print("Proxies={}".format(proxies))            
            with open("location.json", 'r') as f:
                data=json.load(f)
                district_id=data['district_id']                
            proxy = proxies[random.randint(0, len(proxies)-1)]
            sleep(2)
            if not proxy=="": print("Using proxy {}...{}".format(proxy, " "*20), end="\r")
            response=cowin_get(district_id,"{}-{}-{}".format(datetime.date.today().day, datetime.date.today().month, datetime.date.today().year), requests, proxy)
            if response.status_code == requests.codes.ok:
                resp_json=dict(response.json())
                # print(print_centres(resp_json['centers']))
                # print(json.dumps(resp_json, indent=2))
                # new_message = print_centres(resp_json['centers'])
                new_message = print_centres(available_centres(resp_json))
                print("{}".format(new_message), end="")
                if not new_message=="":
                    print("Fetching Telegram API...{}".format(" "*20), end="\r")
                    telegram_bot_sendtext("{}\n\nhttps://selfregistration.cowin.gov.in/".format(new_message))
                else:
                    print("No available centres...{}".format(" "*20), end='\r')
            # print("Waiting 5 seconds...", end="\r")
            sleep(2)
        except:
            print("API error, retrying{}".format(" "*20), end="\r")
            sleep(2)

