# Fitbit API Tips & Pointers

A refresh token does not expire until it is used. The refresh token can only be used once, as a new refresh token is returned with the new access token. If the application makes identical refresh token requests within a two-minute period, the Fitbit Web API will return the same response.

Access tokens created through the authorization code grant flow have a lifespan of 8 hours.  

When the user’s access token expires after 8 hours, need to refresh token to obtain a new access token.

## Sleep
Pay attention to log type.  Either..
-  "logType": "auto_detected"
-  "logType": "manual"

Auto_detected implies the measurement was automatically taken by the fitbit. No adjustments made.

Manual means the data has been adjusted by somebody. It could be a correction (i.e. fitbit battery died, didn't wear the fitbit to bed, etc.). 

A majority of sleep logs (80%+) should be auto_detected. If manually adjusted, lose sleep stage data.