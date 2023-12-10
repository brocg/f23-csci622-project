## Polar API Connection Guide

### 1. Obtain Authorization Code

```
https://polarremote.com/v2/oauth2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI
```

### 2. Exchange Authorization Code for Access Token

request
```
import requests, json, sys, base64

headers = {
    'Accept': 'application/json;charset=UTF-8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Basic {base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}'
}

data = {
    "grant_type": "authorization_code",
    "code": YOUR_AUTHORIZATION_CODE,
    "redirect_uri": "http://localhost"
}

response = requests.post('https://polarremote.com/v2/oauth2/token', headers=headers, data=data)
```

response
```
{
    "access_token": ".................",
    "token_type": "bearer",
    "expires_in": 315359999,
    "x_user_id": 123456
}
```


### 3. Fetch User Basic Information

request
```
headers = {
    "Authorization": f"Bearer {YOUR_ACCESS_TOKEN}",
    "Accept": "application/json"
}

user_id = YOUR_USER_ID
response = requests.get(f"https://polarremote.com/v3/users/{user_id}", headers=headers)
```

response
```
{
    "user_id": 123456,
    "username": "john_doe",
    // other user information...
}
```