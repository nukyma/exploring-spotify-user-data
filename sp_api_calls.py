import json

import spotify_urls


def get_user_private_info(sp):
    """
    get user private profile information
    :param sp:
    :return: result
    """
    endpoint_url = spotify_urls.USER_PRIVATE_INFO
    result = sp.get(endpoint_url)

    return json.loads(result.text)


def get_user_recently_played_tracks(sp):
    """
    get user last 50 played tracks
    :param sp:
    :return:
    """
    endpoint_url = spotify_urls.USER_RECENTLY_PLAYED_TRACKS
    result = sp.get(endpoint_url)

    return json.loads(result.text)
