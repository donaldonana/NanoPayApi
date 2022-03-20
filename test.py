import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

# r = requests.get("https://apiforproject.herokuapp.com/api/UserProfile/")

# print(r.status_code)
# print('----------------')
# print(r.text)
# print('----------------')

data = {
  "email": "monmail@gmail.com",
  "nom": "onana",
  "prenom": "",
  "phone": "60889",
  "password":"123456",
  "avatar" : ""
}

multipart_data = MultipartEncoder(
 fields={
  "email": "monmail@gmail.com",
  "nom": "onana",
  "prenom": "",
  "phone": "60889",
  "password":"123456",
  "avatar" : ""
}

)


r = requests.post("http://127.0.0.1:8000/api/UserProfile/" ,  data = data)
# r = requests.post("http://127.0.0.1:8000/api/UserProfile/" ,  data=multipart_data,
#                   headers={'Content-Type': multipart_data.content_type})

print(r.status_code)
print('----------------')
print(r.text)
print('----------------')