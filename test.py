import requests
import json

# r = requests.get("https://apiforproject.herokuapp.com/api/UserProfile/")

# print(r.status_code)
# print('----------------')
# print(r.text)
# print('----------------')

data = {
		"password" : "0123"}





#r = requests.post("http://127.0.0.1:8000/api/UserProfile/" ,  data = data)
# r = requests.post("http://127.0.0.1:8000/api/UserProfile/" ,  data=multipart_data,
#                   headers={'Content-Type': multipart_data.content_type})

r = requests.post("http://127.0.0.1:8000/api/user/0123/" ,  data = data)

print(r.status_code)
print('----------------')
print(r.text)
print('----------------')
#print(r.headers)
print('----------------')