import requests, ast, copy, datetime, json, random
from time import sleep
from math import remainder

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
    return "\n    Date: {}\n    Ages: {} plus\n    Available Capacity: {}\n    Type: {}".format(session['date'], session['min_age_limit'], session['available_capacity'], session['vaccine'])#, print_slots(session['slots']))

def print_vaccine(vaccines):
    text="\n    Vaccines: "
    offset=len(text)
    offset_text=""
    for i in range(offset):
        offset_text+=" "
    i=0
    for vaccine in vaccines:
        text+= ("\n{}".format(offset_text) if i else "") + "{} - ₹{}".format(vaccine['vaccine'], vaccine['fee'])
        i+=1
        if i==len(vaccines):
            text+="\n"
    # text+="]"
    return text

def print_centres(centres):
    text=""
    for centre in centres:
        # print(len(text))
        text+=("\n\n{}: ".format(centre['name']) if len(text) else "{}: ".format(centre['name']))
        if not len(centre['sessions']):
            text+="\nNo slots avaiable"
        else:
            try:
                # print('paid')
                text+="{}".format(print_vaccine(centre['vaccine_fees']))
                # print(print_vaccine(centre['vaccine_fees']))
            except Exception as e:
                pass
                # print(e, end='\r')
            i=1
            for session in centre['sessions']:
                text+="{}".format(print_session(session))
                if not i==len(centre['sessions']):
                    text+='\n'
                i+=1
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
                new_centre['sessions'].append(session)
                # print(centre['name'], session, sep="\n")
        if len(new_centre['sessions']):
            centres.append(new_centre)
    return centres



def telegram_bot(request, bot_message, opt=0):
    # bot_token = ''
    # bot_chatID = ''
    with open("token.json", 'r') as f:
        tokens=json.load(f)
        bot_token=tokens['bot_token']
        bot_chatID=tokens['bot_chatID']
        bot_msgID=tokens['bot_msgID']
    if request=='sendMessage':
        if opt==0:
            send_text = 'https://api.telegram.org/bot' + str(bot_token) + '/sendMessage?chat_id=' + str(bot_chatID) + '&parse_mode=Markdown&text=' + str(bot_message)
        elif opt==1:
            send_text = 'https://api.telegram.org/bot' + str(bot_token) + '/sendMessage?chat_id=' + str(bot_msgID) + '&parse_mode=Markdown&text=' + str(bot_message)
    elif request=='deleteMessage':
        if opt==0:
            send_text = 'https://api.telegram.org/bot' + str(bot_token) + '/deleteMessage?chat_id=' + str(bot_chatID) + '&message_id=' + str(bot_message)
        elif opt==1:
            send_text = 'https://api.telegram.org/bot' + str(bot_token) + '/deleteMessage?chat_id=' + str(bot_msgID) + '&message_id=' + str(bot_message)
    response = requests.get(send_text)

    return response.json()

def telegram_bot_send(message, opt=0):
    MAX_CHAR=4096
    responses=[]
    # try:
    if len(message)>MAX_CHAR:
        for message_bit in range(0, len(message), MAX_CHAR):
            responses.append(telegram_bot('sendMessage', message[message_bit: message_bit+MAX_CHAR], opt)['result']['message_id'])
    else:
        responses.append(telegram_bot('sendMessage', message, opt)['result']['message_id'])
    return responses
    # except Exception as e:
    #     print(e)  

def telegram_bot_delete(messages, opt=1):
    ok=True
    for message_id in messages:
        response=telegram_bot('deleteMessage', message_id, opt)
        if not response['ok']:
            ok=False
    return ok

messages=[]
if __name__=="__main__":
    false_count=0
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
            # messages.append(telegram_bot('sendMessage', "Fetching CoWin API...", opt=1)['result']['message_id'])            
            if not proxy=="": print("Using proxy {}...{}".format(proxy, " "*20), end="\r")
            response=cowin_get(district_id,"{}-{}-{}".format(datetime.date.today().day, datetime.date.today().month, datetime.date.today().year), requests, proxy)
            if response.status_code == requests.codes.ok:
                # resp={}
                # with open("output.json", 'r') as f:
                #     resp=json.load(f)
                resp_json=dict(response.json())
                # resp_json=resp
                # print(print_centres(resp_json['centers']))
                # print(json.dumps(resp_json, indent=2))
                # new_message = print_centres(resp_json['centers'])
                new_message = print_centres(available_centres(resp_json))
                if not new_message=="":
                    print("{}".format(new_message), end='')
                    print("Fetching Telegram API...{}".format(" "*20), end="\r")
                    telegram_bot('sendMessage', "{}\n\nhttps://selfregistration.cowin.gov.in/".format(new_message))
                else:
                    print("{}{}".format(false_count, " "*20), end='\r')
                    sleep(0.25)
                    alt=1
                    if not remainder(false_count, alt):
                        print("Sending telegram message...".format(" "*20), end='\r')
                        sleep(0.25)
                        new_message = print_centres(resp_json['centers'])
                        # print(new_message)
                        with open("output.json", 'w+') as f:
                            json.dump(resp_json, f, indent=2)
                        responses=telegram_bot_send("API Response:\n{}\n\nhttps://selfregistration.cowin.gov.in/".format(new_message), opt=1)
                        # print("\n{}, {}".format(responses, type(responses)))
                        messages.extend(responses)
                        # print(telegram_bot('sendMessage', "{}\n\nhttps://selfregistration.cowin.gov.in/".format(new_message), opt=1))
                        telegram_bot_delete(messages[:-(len(responses))], 1)
                        messages=messages[-len(responses):]
                    elif remainder(false_count, alt)==-1:
                        false_count=-1
                    false_count+=1
                    print("No available centres...{}".format(" "*20), end='\r')
            # print("Waiting 5 seconds...", end="\r")
            sleep(3)
        except Exception as e:
            telegram_bot_delete(messages, 1)
            print("API error, retrying{}".format(" "*20), end="\r")
            print('\'{}\'{}'.format(e," "*40))
            sleep(3)
            telegram_bot('sendMessage', "Error:\n\n{}".format(e), opt=1)

