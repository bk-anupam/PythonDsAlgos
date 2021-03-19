from requests_oauthlib import OAuth1Session
import webbrowser
import random
from urllib.parse import parse_qsl, urlparse, urlencode


consumer_key = "your consumer key"
consumer_secret = "your consumer secret"
authorization_url = 'https://api.twitter.com/oauth/authorize'
authenticate_url = 'https://api.twitter.com/oauth/authenticate'
# twitter endpoint to get request token
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
callback_uri='https://github.com/bk-anupam'


def twitter_authorization():
    oauth_session = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret, callback_uri=callback_uri)
    rt = oauth_session.fetch_request_token(request_token_url)
    auth_url = oauth_session.authorization_url(authorization_url)
    print("authorization url: {}".format(auth_url))
    redirect_response = input('redirect uri')
    response_param_dict = oauth_session.parse_authorization_response(redirect_response)
    print(response_param_dict)


def get_resource_token():
    #create an object of OAuth1Session
    request_token = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)
    # get request_token_key, request_token_secret and other details
    #rt = request_token.fetch_request_token(url)
    data = request_token.get(request_token_url)
    # split the string to get relevant data
    data_token = str.split(data.text, '&')
    ro_key = str.split(data_token[0], '=')
    ro_secret = str.split(data_token[1], '=')
    resource_owner_key = ro_key[1]
    resource_owner_secret = ro_secret[1]
    resource = [resource_owner_key, resource_owner_secret]
    return resource


def get_resource_token2():
    auth_params = {
        "client_id": consumer_key,
        "state": str(random.getrandbits(64)),  # to protect from CSRF
        "redirect_uri": 'https://github.com/bk-anupam',
        "scope": "email",  # we want to get access to email
        "response_type": "code",
    }
    AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
    url = "?".join([AUTHORIZE_URL, urlencode(auth_params)])
    print(url)
    webbrowser.open_new_tab(url)
    redirected_url = input("Paste here url you were redirected:\n")
    redirect_params = dict(parse_qsl(urlparse(redirected_url).query))
    assert redirect_params['state'] == auth_params['state']  # protect CSRF
    auth_code = redirect_params['code']
    print("auth_code: {}".format(auth_code))


def twitter_get_oauth_token(verifier, ro_key, ro_secret):
    oauth_token = OAuth1Session(client_key=consumer_key,
                                client_secret=consumer_secret,
                                resource_owner_key=ro_key,
                                resource_owner_secret=ro_secret)
    url = 'https://api.twitter.com/oauth/access_token'
    data = {"oauth_verifier": verifier}
    print(ro_key)
    print(ro_secret)
    access_token_data = oauth_token.post(url, data=data)
    print(access_token_data.text)
    access_token_list = str.split(access_token_data.text, '&')
    return access_token_list


def twitter_get_access_token(access_token_list):
    access_token_key = str.split(access_token_list[0], '=')
    access_token_secret = str.split(access_token_list[1], '=')
    access_token_name = str.split(access_token_list[3], '=')
    access_token_id = str.split(access_token_list[2], '=')
    key = access_token_key[1]
    secret = access_token_secret[1]
    name = access_token_name[1]
    id = access_token_id[1]
    oauth_user = OAuth1Session(client_key=consumer_key,
                               client_secret=consumer_secret,
                               resource_owner_key=key,
                               resource_owner_secret=secret)
    url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    params = {"include_email": 'true'}
    user_data = oauth_user.get(url_user, params=params)
    print(user_data.json())
    return user_data.json()


if __name__ == "__main__":
    #twitter_authorization()
    #resource = get_resource_token()
    #print("resource owner key = {}, resource owner secret = {}".format(resource[0], resource[1]))
    #redirect_url = authenticate_url + "?oauth_token=" + resource[0]
    #print("Redirect url = {}".format(redirect_url))
    access_token_l = twitter_get_oauth_token('verifier', 'ro_key', 'ro_secret')
    print(access_token_l)
    twitter_get_access_token(access_token_l)