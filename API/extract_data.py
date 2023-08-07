import json

import API.endpoints


def get_user_private_info(sp):
    """
    get user private profile information
    :param sp: authorize spotify session
    :return type(json): private user info
    """
    endpoint_url = API.endpoints.USER_PRIVATE_INFO
    result = sp.get(endpoint_url)

    return json.loads(result.text)


def get_user_recently_played_tracks(sp):
    """
    get user last 50 played tracks
    :param sp: authorize spotify session
    :return type(json): items dict size 50 with tracks info
    """
    endpoint_url = API.endpoints.USER_RECENTLY_PLAYED_TRACKS
    result = sp.get(endpoint_url)

    return json.loads(result.text)


def get_several_tracks_info(sp, batch_ids):
    """
    get the all track info
    :param sp: authorize spotify session
    :param str batch_ids: A comma-separated list of the Spotify IDs
    :return type(json): items dict size 50 with tracks info
    """

    endpoint_url = API.endpoints.SEVERAL_TRACKS_INFO
    result = sp.get(endpoint_url + batch_ids)

    return json.loads(result.text)


def get_several_audio_features_info(sp, batch_ids):
    """
    get audio features info
    :param sp: authorize spotify session
    :param str batch_ids: A comma-separated list of the Spotify IDs
    :return type(json): items dict size 50 with tracks info
    """

    endpoint_url = API.endpoints.SEVERAL_AUDIO_FEATURES
    result = sp.get(endpoint_url + batch_ids)

    return json.loads(result.text)


def get_several_artists_info(sp, batch_ids):
    """
    get artist info
    :param sp: authorize spotify session
    :param batch_ids: A comma-separated list of the Spotify IDs
    :return json: items dict size 50 with artist info
    """

    endpoint_url = API.endpoints.SEVERAL_ARTISTS_INFO
    result = sp.get(endpoint_url + batch_ids)

    return json.loads(result.text)
