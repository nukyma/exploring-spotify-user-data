from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

import settings
from API import extract_data
from DATABASE import play_table
from TRANSFORM import transform_data

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
    user_info = extract_data.get_user_private_info(sp=spotify)

    # Extract
    played_tracks = extract_data.get_user_recently_played_tracks(sp=spotify)
    # Transform: Select, clean and transform data
    played_tracks_dict = transform_data.recently_played_tracks(data=played_tracks)
    # Load
    play_table.insert_into_play(data=played_tracks_dict)
