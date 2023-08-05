from API import extract_data, connection
from DATABASE import play_table, track_table, audio_features_table
from TRANSFORM import transform_data

import logging

import settings

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, filename=settings.LOGS_FILE_LOCATION, format='%(asctime)s  -  %(message)s')

    # Stablish connection (authentication and authorization) with Spotify API
    try:
        spotify, token = connection.connect_spotify_api()
    except ConnectionError:
        logging.info('Error connecting with Spotify API')

    # Use own methods to pull raw data from the Spotify API
    # user_info = extract_data.get_user_private_info(sp=spotify)

    ###         USER LAST 50 PLAYED SONGS                       ###
    # Extract
    try:
        played_tracks = extract_data.get_user_recently_played_tracks(sp=spotify)
    except RuntimeError:
        logging.info('ENDPOINT NOT WORKING: get_user_recently_played_tracks ')

    # If the response is OK
    try:
        # Select, clean and transform data from the response to populate different tables
        played_tracks, track_info, map_track_album_info, map_track_artist_info = (
            transform_data.recently_played_tracks_response(data=played_tracks))
    except ValueError:
        logging.info('ENDPOINT RESPONSE: get_user_recently_played_tracks status: ', played_tracks['error']['status'])

    ###         COMPLETE AUDIO FEATURES INFO IN BATCHES OF 50    ###
    # Consult our DB
    list_audio_ids = audio_features_table.get_audio_incomplete()
    # BATCH
    list_batch_ids = transform_data.make_batches_of_tracks_ids(size=50, data=list_audio_ids)
    # Extract
    info_audio_features = list()
    for i in list_batch_ids:
        info_audio_features.append(extract_data.get_several_audio_features_info(sp=spotify, batch_ids=i))
    # Transform
    info_audio_features_dict = transform_data.audio_features_info(data=info_audio_features)
    # Load
    audio_features_table.insert_into_audio_features(data=info_audio_features_dict)
