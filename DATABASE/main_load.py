import logging
import sqlite3

import settings


def insert_into_play_audio_features_track_table(data, trigger):
    """
    Insert the play (track_id + played_at + context) in play table
    Insert track_id in audio_features
    If trigger param is set to True, then the track_id and played_at is inserted in the track table as follows:
    - If the track was already in the table, updates the last_play field and sums 1 to times_played
    - If the track is not in the table, then adds the track_id, the first_play = last_play which is played_at
      and times_played is equal to 1
    :param list of dict data: response from recently_played_tracks_response endpoint
    :param trigger: flag use to trigger the insert into the track table
    """
    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    for d in data:

        # Check if the pair (track_id and played_at) are already on the table play
        sql_select_ = '''SELECT track_id, track_played_at 
                         FROM play 
                         WHERE track_id = ? AND track_played_at = ? '''
        par_select_ = (d['track_id'], d['played_at'])

        cur.execute(sql_select_, par_select_)

        # If pair (track_id and played_at) ARE NOT in the DB, we should include them in play table
        # And we should include the track_id in audio_features table as well
        if not cur.fetchone():
            sql_insert_play_ = '''INSERT INTO play (track_id, track_played_at, context) 
                                  VALUES (?, ?, ?)'''
            par_insert_play_ = (d['track_id'], d['played_at'], d['context'])

            cur.execute(sql_insert_play_, par_insert_play_)

            # Insert the track_id in the audio_features table
            # Check if the value is already in the table
            sql_select_ = '''SELECT track_id
                             FROM audio_features
                             WHERE track_id = ? '''
            par_select_ = [d['track_id']]

            cur.execute(sql_select_, par_select_)

            # If track_id not in the table, then insert it
            if not cur.fetchone():
                sql_insert_track_features_ = '''INSERT INTO audio_features (track_id)
                                            VALUES (?)'''

                cur.execute(sql_insert_track_features_, [d['track_id']])

            # TRIGGER track TABLE
            if trigger:
                # Search for the track in the track table
                sql_search_track_ = "SELECT name FROM track WHERE id = ? "
                par_search_track_ = [d['track_id']]

                cur.execute(sql_search_track_, par_search_track_)

                # IF the track is in the table already, we should update the last_played and times_played fields
                # And we may suppose that the rest of the track info is already there
                if cur.fetchone():
                    sql_update_track_ = ''' UPDATE track 
                                            SET last_played = ?, times_played = times_played+1
                                            WHERE id = ? '''
                    par_update_track_ = (d['played_at'], d['track_id'])

                    cur.execute(sql_update_track_, par_update_track_)

                # IF NOT, the track should be inserted in the track table:
                # track_id, first_played = last_played and times played = 1
                else:
                    sql_insert_track_ = '''INSERT INTO track (id, first_played, last_played, times_played) 
                                           VALUES (?, ?, ?, 1)'''
                    par_insert_track_ = (d['track_id'], d['played_at'], d['played_at'])

                    cur.execute(sql_insert_track_, par_insert_track_)

    con.commit()
    con.close()


def upload_track_table(data):
    """
    Function that uploads data in the track table.
    :param list of dict data:
    :return:
    """
    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    for d in data:

        # Check the track_id is already in the table but the information is incompleted
        # Check if the value is already in the table and incomplete
        sql_select_ = '''SELECT id, name
                         FROM track
                         WHERE id = ? '''
        par_select_ = [d['id']]

        cur.execute(sql_select_, par_select_)

        # id is in table but info incomplete (name=None). We should update it.
        if cur.fetchone()[1] is None:
            sql_update_track_ = '''UPDATE track
                                   SET name = ?, 
                                       album_id = ?,
                                       album_name = ?,
                                       artists_id = ?,
                                       artists_names = ?,
                                       duration_ms = ?,
                                       explicit = ?,
                                       type = ?,
                                       preview_url = ? 
                                    WHERE id = ? '''

            par_update_track_ = (d['name'],
                                 d['album_id'],
                                 d['album_name'],
                                 d['artists_id'],
                                 d['artists_names'],
                                 d['duration_ms'],
                                 d['explicit'],
                                 d['type'],
                                 d['preview_url'],
                                 d['id'])

            cur.execute(sql_update_track_, par_update_track_)

    con.commit()
    con.close()


def insert_into_map_track_album_table(data):
    """
    Function that checks if the track_id and album_id are already in the table and if not insert the info
    :param list of dict data: Contains track_id, album_id, played_at, context
    """
    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    for d in data:

        # Check if the values are already in the table
        sql_select_map_track_album_ = '''SELECT track_id, album_id
                         FROM map_track_album
                         WHERE track_id = ? AND album_id = ?'''
        par_select_map_track_album_ = (d['track_id'], d['album_id'])

        cur.execute(sql_select_map_track_album_, par_select_map_track_album_)

        if not cur.fetchone():
            sql_map_track_album_ = '''INSERT INTO map_track_album (track_id, album_id, played_at, context)
                                       VALUES (?, ?, ?, ?)'''
            par_map_track_album_ = (d['track_id'], d['album_id'], d['played_at'], d['context'])

            cur.execute(sql_map_track_album_, par_map_track_album_)

    con.commit()
    con.close()


def insert_into_map_track_artist_table(data):
    """
    Function that checks if the track_id and artist_id are already in the table and if not insert the info
    :param list of dict data: Contains track_id, artist_id, played_at, context
    """
    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    for d in data:

        # Check if the values are already in the table
        sql_select_map_track_artist_ = '''SELECT track_id, artist_id
                         FROM map_track_artist
                         WHERE track_id = ? AND artist_id = ?'''
        par_select_map_track_artist_ = (d['track_id'], d['artist_id'])

        cur.execute(sql_select_map_track_artist_, par_select_map_track_artist_)

        if not cur.fetchone():
            sql_map_track_artist_ = '''INSERT INTO map_track_artist (track_id, artist_id, played_at, context)
                                       VALUES (?, ?, ?, ?)'''
            par_map_track_artist_ = (d['track_id'], d['artist_id'], d['played_at'], d['context'])

            cur.execute(sql_map_track_artist_, par_map_track_artist_)

    con.commit()
    con.close()


def get_artists_ids_from_map_table():
    """
    Function that gets the artists ids from the map_track_table from 2 days before now
    :return list artist_id: list of artists ids
    """
    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    sql_select_ = '''SELECT DISTINCT artist_id
                     FROM map_track_artist
                     WHERE strftime('%Y-%m-%d %H:%M:%f', played_at) >= DATETIME('now', '-2 day')'''

    cur.execute(sql_select_)
    response = cur.fetchall()

    if response:
        artist_id_list = list()
        for i in response:
            artist_id_list.append(i[0])
    else:
        artist_id_list = None

    return artist_id_list


def insert_into_artist(data):
    """
    Function that gets data pre-transform to load it in the artist table.
    Before insert, it checks if the info is already there to no violate unique constraint
    :param data: dictionary with pre-transform artist data
    """
    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    for d in data:

        try:
            # Check if the values are already in the table
            sql_select_artist_ = '''SELECT id
                             FROM artist
                             WHERE id = ? '''
            par_select_artist_ = [d['id']]

            cur.execute(sql_select_artist_, par_select_artist_)

        except ValueError:
            logging.info('DATABASE: Check if artist id is already in the table at insert_info_artist')

        if not cur.fetchone():

            try:
                sql_insert_artist_ = '''INSERT INTO artist (id, name, genres, followers, external_urls)
                                           VALUES (?, ?, ?, ?, ?)'''
                par_insert_artist_ = (d['id'], d['name'], d['genres'], d['followers'], d['external_urls'])

                cur.execute(sql_insert_artist_, par_insert_artist_)

            except ValueError:
                logging.info('DATABASE: insert into artist table failed at insert_into_artist')

    con.commit()
    con.close()
