import logging
import sqlite3
from time import sleep

import settings
from API import extract_data, connection
from DATABASE import main_db_queries
from TRANSFORM import transform_data


def extra_complete_artists_from_tracks():
    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    logging.info("1/8 Getting artists_ids from track table")
    sql_select_track_ids_ = ''' SELECT DISTINCT id, artists_id
                                FROM track
                                GROUP BY 1
                                '''

    cur.execute(sql_select_track_ids_)
    response_track = cur.fetchall()

    logging.info("2/8  Formatting the query result to obtain a list of ids")
    artist_id_list = list()
    for i in response_track:
        artist = i[1]
        artist = artist.replace('[', '')
        artist = artist.replace(']', '')
        artist = artist.replace(' ', '')
        artist = artist.replace('"', '')
        artist = artist.replace("'", '')
        aux_list = list(artist.split(','))

        for j in aux_list:
            artist_id_list.append(j)

    logging.info("3/8  Removeing duplicates ids by transforming list to set and back to list")
    artist_id_list = [elem for elem in set(artist_id_list)]

    logging.info("4/8  Checking if id already in artist table. If so, remove id from list")
    for k in artist_id_list:
        sql_select_artist_id_ = ''' SELECT id
                                    FROM artist
                                    WHERE id = ?
                                '''
        par_select_artist_id_ = [k]
        cur.execute(sql_select_artist_id_, par_select_artist_id_)

        response_artist = cur.fetchone()

        # Remove the artist id already in the table
        if response_artist:
            artist_id_list.remove(k)

    # Call the endpoint to get the info for the artists remain in artist_id_list
    logging.info(f"5/8  There are {len(artist_id_list)} artists ids that need to complete their information")

    if artist_id_list:
        # Chunk artist ids list into batches
        artists_ids_batched = transform_data.make_batches_of_tracks_ids(size=50, data=artist_id_list)

        # Call the endpoint to get artist info data
        logging.info("6/8 Request to the API endpoint as many times as batches ")
        info_artists = list()
        for artist_batch in artists_ids_batched:
            sleep(1.11)
            try:
                info_artists.append(extract_data.get_several_artists_info(sp=spotify, batch_ids=artist_batch))
            except ValueError:
                logging.error('ENDPOINT: response get_several_artists_info status: ', info_artists)
    else:
        logging.error('DATA: no data retrieve from artists_ids_from_map_table query')

    logging.info("7/8 Transform and format response data")
    # Transform the response into the data format we need to store it in the DB
    info_artists_dict = transform_data.artist_info(data=info_artists)

    # Load the data into the data base
    logging.info("8/8 Loding data response into DB")
    try:
        main_db_queries.insert_into_artist(data=info_artists_dict)
    except ValueError:
        logging.error('DATABASE: Error loading info_artists_dict to artist table')

    con.close()


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO,
                        filename=settings.LOG_CAFTT_FILE_LOCATION,
                        format='%(asctime)s  -  %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('Extra Function --> extra_complete_artists_from_tracks')
    logging.info('0/8 Open connection with spotify api')

    try:
        spotify, token = connection.connect_spotify_api()
    except ConnectionError:
        logging.error('Error connecting with Spotify API')

    extra_complete_artists_from_tracks()

    logging.info('The execution has finished successfully %(asctime)s ')
