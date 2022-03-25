import requests
import json

# r = requests.get("https://apiforproject.herokuapp.com/api/UserProfile/")

# print(r.status_code)
# print('----------------')
# print(r.text)
# print('----------------')

data = {"username" : "000",
		"password" : "000"}





#r = requests.post("http://127.0.0.1:8000/api/UserProfile/" ,  data = data)
# r = requests.post("http://127.0.0.1:8000/api/UserProfile/" ,  data=multipart_data,
#                   headers={'Content-Type': multipart_data.content_type})

r = requests.post("http://127.0.0.1:8001/api/api-token-auth/" ,  data = data)

print(r.status_code)
print('----------------')
print(r.text)
print('----------------')
print(r.headers)
print('----------------')