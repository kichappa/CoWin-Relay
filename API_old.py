import requests, json, hashlib, pathlib
from secret import encrypt

password = "CoWIN@$#&*(!@%^&".encode()
username="b5cab167-7977-4df1-8027-a63aa144f04e".encode()

token=encrypt(username, password).decode()
print(token)


with open("mobile.json", "r") as f:
    mobile=json.load(f)['mobile']

# URL = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"
# response = requests.post(URL, json={
#     "mobile": mobile,
#     "secret": token
# }, headers={
#     "accept": "application/json",
#     "Accept-Language": "en_US",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
#     })

# print(response)
# print(response.json())
# otp=str(input("Enter OTP: "))
# otpHash=hashlib.sha256(otp.encode()).hexdigest()
# print(otp, otpHash)

# URL = "https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp"
# response = requests.post(URL, json={
#     "otp": otpHash,
#     "txnId": response.json()['txnId']
# }, headers={
#     "accept": "application/json",
#     "Accept-Language": "en_US",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
#     })

# print(response)
# print(response.json())

# bearer_token=response.json()['token']
# with open("token.json", 'w+') as f:
#     json.dump(response.json(),f, indent=2)

with open("token.json", 'r') as f:
    response = json.load(f)
bearer_token=response['token']

URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=307&date=20-05-2021"
response = requests.get(URL, headers={
    "accept": "application/json",
    "Accept-Language": "en_US",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "authorization": "Bearer {}".format(bearer_token)
    })

print(response)
print(response.json())

URL = "https://cdn-api.co-vin.in/api/v2/appointment/centers/findByLatLong?lat=27&long=76"
response = requests.get(URL, headers={
    "accept": "application/json",
    "Accept-Language": "en_US",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "authorization": "Bearer {}".format(bearer_token)
    })

print(response)
print(response.content)

URL = "https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"
response = requests.get(URL, headers={
    "accept": "application/json",
    "Accept-Language": "en_US",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "authorization": "Bearer {}".format(bearer_token)
    })

print(response)
print(response.json())

URL = "https://cdn-api.co-vin.in/api/v2/registration/certificate/download?beneficiary_reference_id={}".format(response.json()['beneficiaries'][0]['beneficiary_reference_id'])
response = requests.get(URL, headers={
    "accept": "application/json",
    "Accept-Language": "en_US",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "authorization": "Bearer {}".format(bearer_token)
    })

print(response)
print(response.raw)
# print(response.content)
with pathlib.Path("beni.pdf") as f:
    f.write_bytes(response.content)
# print(response.json())