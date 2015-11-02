import twitter
def oauth_login_0():
    CONSUMER_KEY = 'ijPhrWnWnYYkiSAIcGG71AoI3'
    CONSUMER_SECRET = 'eYxAtY0rD5YCZymSw4Pz09IkbexMRPaDd8SnKdVZfdxRNW6kwH'
    OAUTH_TOKEN = '2802939841-JvNUWc5V1RhR7EHULgtdViAuI7fqEwHfccvkYba'
    OAUTH_TOKEN_SECRET = 'feg6w5sUbm7JUjS4MVbJmaJKnosErIQiR1I4ffNDQb94Y'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

def oauth_login_1():
    CONSUMER_KEY = '0F7M0XwvvFtaaIGaL3D9OT0QS'
    CONSUMER_SECRET = '5mi0Ga1QF8dYOO0UKBGguvvwqI8IRfk1MQPnQR3p5y6nQlk4Gk'
    OAUTH_TOKEN = '902037876-vMYZxHcQqreKskOK1u1sdn7tzA3QaueYLTT1JTyJ'
    OAUTH_TOKEN_SECRET = '7URGMvLmTlsVrCVrJJRC7Cx0eM9Uc0tSkL7M4GsncpVSJ'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

