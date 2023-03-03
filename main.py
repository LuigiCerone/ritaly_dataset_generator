import requests
import os

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

data = {'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD}

headers = {'User-Agent': 'MyBot/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

res = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
print(res.json())
