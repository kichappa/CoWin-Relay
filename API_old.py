import requests, json, hashlib, pathlib, datetime
from secret import encrypt

password = "CoWIN@$#&*(!@%^&".encode()
username="b5cab167-7977-4df1-8027-a63aa144f04e".encode()

token=encrypt(username, password).decode()
print(token)

def _get_response(method, headerAppend={}, **kwargs):
    with open("api.json", "r") as f:
        apiJSON=json.load(f)
        request={**apiJSON[method], "header": {**apiJSON["genericHeaders"], **headerAppend}}

    
    for key, value in kwargs.items():
        try:
            if type(request[key])==str:
                request[key]=request[key].format(**value)
        except Exception as e:
            print(e)
        
    if request["type"]=="POST":
        request["json"]=kwargs["json"]

    # print(json.dumps(request, indent=2))

    if request["type"]=="POST":
        return requests.post(url=request['url'], json=request['json'], headers=request['header'])
    elif request["type"]=="GET":
        return requests.get(url=request['url'], headers=request['header'])

def _today():
    return "{}-{}-{}".format(datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)

with open("mobile.json", "r") as f:
    mobile=json.load(f)['mobile']
    
response = _get_response("generateMobileOTP", json={
    "mobile": mobile,
    "secret": token
})

print(response)
try:
    print(response.json())
except:
    print(response.content)

otp=str(input("Enter OTP: "))
otpHash=hashlib.sha256(otp.encode()).hexdigest()
print(otp, otpHash)

response = _get_response("validateMobileOTP", json={
    "otp": otpHash,
    "txnId": response.json()['txnId']
})

print(response)
try:
    print(response.json())
except:
    print(response.content)

bearer_token=response.json()['token']
with open("token.json", 'w+') as f:
    json.dump(response.json(),f, indent=2)

# with open("token.json", 'r') as f:
#     response = json.load(f)
# bearer_token=response['token']

response = _get_response("calendarByDistrict", headerAppend={
    "authorization": "Bearer {}".format(bearer_token)
}, url={
    "district_id": 307, 
    "date": _today()
})

print("\n\nCalender By District")
print(response)
try:
    print(response.json())
except:
    print(response.content)

response = _get_response("findByDistrict", headerAppend={
    "authorization": "Bearer {}".format(bearer_token)
}, url={
    "district_id": 307, 
    "date": _today()
})

print("\n\nFind By District")
print(response)
print(response.json())

response = _get_response("calendarByPIN", headerAppend={
    "authorization": "Bearer {}".format(bearer_token)
}, url={
    "pincode": 682024, 
    "date": _today()
})

print("\n\nCalender By PIN")
print(response)
print(response.json())

response = _get_response("findByPIN", headerAppend={
    "authorization": "Bearer {}".format(bearer_token)
}, url={
    "pincode": 682024, 
    "date": _today()
})

print("\n\nFind By PIN")
print(response)
print(response.json())

response = _get_response("beneficiaries", headerAppend={
    "authorization": "Bearer {}".format(bearer_token)
})

print(response)
try:
    print(response.json())
except:
    print(response.content)
    
URL = "https://cdn-api.co-vin.in/api/v2/registration/certificate/download?beneficiary_reference_id={}".format(response.json()['beneficiaries'][1]['beneficiary_reference_id'])
response = _get_response("certificate", headerAppend={
    "authorization": "Bearer {}".format(bearer_token)
}, url={
    "beneficiary_reference_id": response.json()['beneficiaries'][1]['beneficiary_reference_id']
})

print(response)
with pathlib.Path("beni.pdf") as f:
    f.write_bytes(response.content)