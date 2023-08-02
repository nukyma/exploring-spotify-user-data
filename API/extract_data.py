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
