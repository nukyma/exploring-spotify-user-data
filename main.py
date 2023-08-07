import logging
from time import sleep

import settings
from API import extract_data, connection
from DATABASE import main_db_queries
from TRANSFORM import transform_data

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, filename=settings.LOGS_FILE_LOCATION, format='%(asctime)s  -  %(message)s')

    # Stablish connection (authentication and authorization) with Spotify API
    try:
        spotify, token = connection.connect_spotify_api()
    except ConnectionError:
        logging.info('Error connecting with Spotify API')

    # Use own methods to pull raw data from the Spotify API
    # user_info = extract_data.get_user_private_info(sp=spotify)

    ##         USER LAST 50 PLAYED SONGS                       ###

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
        main_db_queries.insert_into_play_audio_features_track_table(data=played_tracks, trigger=True)
        main_db_queries.upload_track_table(data=track_info)
        main_db_queries.insert_into_map_track_album_table(data=map_track_album_info)
        main_db_queries.insert_into_map_track_artist_table(data=map_track_artist_info)
    except ValueError:
        logging.info('LOAD DB ERROR: loading data from endpoint response get_user_recently_played_tracks')

    ###         COMPLETE ARTIST INFO                              ###
    # Query the map_track_artist table to get the artists ids that are going to be in the query
    # We should query artist that have been included 2 days before now
    try:
        artists_ids_list = main_db_queries.get_artists_ids_from_map_table()
    except ValueError:
        logging.info('DATABASE: Select artists_ids_from_map_table query failed')

    if artists_ids_list:
        # Chunk artist ids list into batches
        artists_ids_batched = transform_data.make_batches_of_tracks_ids(size=50, data=artists_ids_list)

        # Call the endpoint to get artist info data
        info_artists = list()
        for a in artists_ids_batched:
            sleep(1)
            try:
                info_artists.append(extract_data.get_several_artists_info(sp=spotify, batch_ids=a))
            except ValueError:
                logging.info('ENDPOINT: response get_several_artists_info status: ', info_artists)
    else:
        logging.info('DATA: no data retrieve from artists_ids_from_map_table query')

    # Transform the response into the data format we need to store it in the DB
    info_artists_dict = transform_data.artist_info(data=info_artists)

    # Load the data into the data base
    try:
        main_db_queries.insert_into_artist(data=info_artists_dict)
    except ValueError:
        logging.info('DATABASE: Error loading info_artists_dict to artist table')

    ###         COMPLETE ALBUM INFO                              ###
    # Query the map_track_album table to get the album ids that are going to be in the query
    # We should query albums that have been included 2 days before now
    try:
        album_ids_list = main_db_queries.get_album_ids_from_map_table()
    except ValueError:
        logging.info('DATABASE: get_album_ids_from_map_table query failed')

    if album_ids_list:
        # Chunk artist ids list into batches
        album_ids_batched = transform_data.make_batches_of_tracks_ids(size=20, data=album_ids_list)

        # Call the endpoint to get artist info data
        info_album = list()
        for album_batch in album_ids_batched:
            sleep(1.35)
            try:
                info_album.append(extract_data.get_several_album_info(sp=spotify, batch_ids=album_batch))
            except ValueError:
                logging.info('ENDPOINT: response get_several_album_info status: ', info_album)
    else:
        logging.info('DATA: no data retrieve from get_album_ids_from_map_table query')

    # Transform the response into the data format we need to store it in the DB
    info_album_dict = transform_data.album_info(data=info_album)

    # Load the data into the data base
    try:
        main_db_queries.insert_into_album(data=info_album_dict)
    except ValueError:
        logging.info('DATABASE: Error loading info_album_dict to artist table')

    ###         COMPLETE AUDIO FEATURES INFO IN BATCHES OF 50    ###
    # Consult our DB for incomplete audio_features entries
    try:
        audio_ids_list = main_db_queries.get_audio_incomplete()
    except ValueError:
        logging.info('DATABASE: get_audio_incomplete query failed')

    if audio_ids_list:
        # BATCH
        list_batch_ids = transform_data.make_batches_of_tracks_ids(size=100, data=audio_ids_list)
        # Extract
        info_audio_features = list()
        for audio_batch in list_batch_ids:
            sleep(1.49)
            try:
                info_audio_features.append(
                    extract_data.get_several_audio_features_info(sp=spotify, batch_ids=audio_batch))
            except ValueError:
                logging.info('ENDPOINT: response get_several_audio_features_info status: ', info_audio_features)
    else:
        logging.info('DATA: no data retrieve from get_album_ids_from_map_table query')

    # Transform
    info_audio_features_dict = transform_data.audio_features_info(data=info_audio_features)

    # Load
    try:
        main_db_queries.insert_into_audio_features(data=info_audio_features_dict)
    except ValueError:
        logging.info('DATABASE: Error loading info_album_dict to artist table')

logging.info('End of main')
