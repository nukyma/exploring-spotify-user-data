import json

import API.url_constants


def get_user_private_info(sp):
    """
    get user private profile information
    :param sp: authorize spotify session
    :return type(json): private user info
    """
    endpoint_url = API.url_constants.USER_PRIVATE_INFO
    result = sp.get(endpoint_url)

    return json.loads(result.text)


def get_user_recently_played_tracks(sp):
    """
    get user last 50 played tracks
    :param sp: authorize spotify session
    :return type(json): items dict size 50 with tracks info
    """
    endpoint_url = API.url_constants.USER_RECENTLY_PLAYED_TRACKS
    result = sp.get(endpoint_url)

    return json.loads(result.text)


def get_several_tracks_info(sp, batch_ids):
    """
    get the all track info
    :param sp: authorize spotify session
    :param str batch_ids: A comma-separated list of the Spotify IDs
    :return type(json): items dict size 50 with tracks info
    """

    endpoint_url = API.url_constants.SEVERAL_TRACKS_ID
    result = sp.get(endpoint_url+batch_ids)

    return json.loads(result.text)
