# Polar API Tips & Pointers
Great documenation found here: https://www.polar.com/accesslink-api/#polar-accesslink-api

Some key takeaways to be aware of after using this for ~2 weeks:
- Polar will only offer data going 30 days back 
- Fetching user data (training, activity and physical information) from Accesslink is based on transactions. To save data you can commit a "transaction" (stores up to 50 activities), then save it on your own
- There are short-term and long-term limits to the API requests

## Rate Limits
Two kind of rate limits: short term (15min) and long term(24h)
- short term limit is reset after 15 minutes have passed since first request is made
- long term limit is reset after 24 hours

### Formula for rate limits
Calculating rate limit is based on users.

Base formulas:
- short-term : 500 + number of users * 20
- long-term: 5000 + number of users * 100

So, easy example, assuming you have 1 user (i.e. personal use).
- 15min rate limit: 500 + (1 user) * 20 = 520
- 24h rate limit: 5000 + (1 user) * 100 = 5100

## Authentication & Making Requests
*Note: An important nuance to understand...there's TWO types of authentication for Polar's API Accesslink 3.0

1. Authentication with user token (access token)
2. authentication with client (partner) credentials. 

So pay attention to this as you make requests to different endpoints. Common mistake is to be using the wrong one.

Examples:

- All requests to /v3/users and its subresources are done with user token authentication
    - GET /v3/users/...

        Name | Value
        -----|-------
        Authorization | Bearer `<access-token>`

- All other /v3/ requests (/v3/notifications for example) are done with client credentials.
    - GET /v3/...

        Name | Value
        -----|-------
        Authorization | Basic `dGhpc2RvZXNuM3V0dGVyYXRoYW5ncGVhbnV0YnV0dGVy`

        Where `dGhpc2RvZXNuM3V0dGVyYXRoYW5ncGVhbnV0YnV0dGVy` is replaced with base64 encoded string client_id:client_secret. For example, if your client id is `12345` and client secret is `verySecret`, then you need to base64 encode string `12345:verySecret`.