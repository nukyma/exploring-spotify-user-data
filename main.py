from API import extract_data, connection
from DATABASE import main_load
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

    # Load
    try:
        main_load.insert_into_play_audio_features_track_table(data=played_tracks, trigger=True)
        main_load.upload_track_table(data=track_info)
        main_load.insert_into_map_track_album_table(data=map_track_album_info)
        main_load.insert_into_map_track_artist_table(data=map_track_artist_info)
    except ValueError:
        logging.info('LOAD DB ERROR: loading data from endpoint response get_user_recently_played_tracks')


    # ###         COMPLETE TRACKS INFO IN BATCHES OF 50           ###
    # # Consult our DB
    # list_tracks_ids = track_table.get_tracks_incomplete()
    # # BATCH
    # list_batch_ids = transform_data.make_batches_of_tracks_ids(size=50, data=list_tracks_ids)
    # # Extract
    # info_tracks = list()
    # for i in list_batch_ids:
    #     info_tracks.append(extract_data.get_several_tracks_info(sp=spotify, batch_ids=i))
    # # Transform
    # info_tracks_dict = transform_data.tracks_info(data=info_tracks)
    # # Load
    # track_table.insert_into_track(data=info_tracks_dict)
    #
    # ###         COMPLETE AUDIO FEATURES INFO IN BATCHES OF 50    ###
    # # Consult our DB
    # list_audio_ids = audio_features_table.get_audio_incomplete()
    # # BATCH
    # list_batch_ids = transform_data.make_batches_of_tracks_ids(size=50, data=list_audio_ids)
    # # Extract
    # info_audio_features = list()
    # for i in list_batch_ids:
    #     info_audio_features.append(extract_data.get_several_audio_features_info(sp=spotify, batch_ids=i))
    # # Transform
    # info_audio_features_dict = transform_data.audio_features_info(data=info_audio_features)
    # # Load
    # audio_features_table.insert_into_audio_features(data=info_audio_features_dict)
