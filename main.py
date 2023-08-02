from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

import settings
from sp_api_calls import get_user_private_info, get_user_recently_played_tracks

if __name__ == '__main__':
    # Create a OAuth2Session named spotify
    spotify = OAuth2Session(client_id=settings.CLIENT_ID,
                            scope=settings.SCOPE,
                            redirect_uri=settings.REDIRECT_URI)

    # Redirect user to Spotify for authorization
    authorization_url, state = spotify.authorization_url(settings.AUTHORIZATION_BASE_URL)
    print('Please go here and authorize: ', authorization_url)

    # Get the authorization verifier code from the callback url paste by the user
    redirect_response = input('\n\nPaste the full redirect URL here: ')

    auth = HTTPBasicAuth(settings.CLIENT_ID, settings.CLIENT_SECRET)

    # Fetch the access token
    token = spotify.fetch_token(settings.TOKEN_URL,
                                auth=auth,
                                authorization_response=redirect_response)

    # Use own methods to pull raw data from the Spotify API
    user_info = get_user_private_info(sp=spotify)
    get_user_recently_played_tracks(sp=spotify)
