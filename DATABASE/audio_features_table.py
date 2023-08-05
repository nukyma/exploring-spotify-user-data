import sqlite3

import settings


def get_audio_incomplete():
    """
    get the tracks id of the tracks which info is not complete
    :return list list_ids: a list of the tracks ids that are incomplete
    """
    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    # Check if the pair (track_id and played_at) are already on the table play
    sql_select_ids_ = '''SELECT track_id
                         FROM audio_features
                         WHERE audio_features.acousticness IS NULL'''

    cur.execute(sql_select_ids_)
    list_ids = list()
    for i in cur.fetchall():
        list_ids.append(i[0])

    return list_ids


def insert_into_audio_features(data):

    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    for d in data:

        sql_update_audio_ = '''UPDATE audio_features
                               SET acousticness = ?, 
                                   analysis_url = ?,
                                   danceability = ?,
                                   energy = ?,
                                   instrumentalness = ?,
                                   duration_ms = ?,
                                   key = ?,
                                   liveness = ?,
                                   loudness = ?,
                                   mode = ?,
                                   valence = ?,
                                   speechiness = ?,
                                   tempo = ?,
                                   time_signature = ?,
                                   track_href = ?
                                WHERE track_id = ? '''

        par_update_audio_ = (d['acousticness'],
                             d['analysis_url'],
                             d['danceability'],
                             d['energy'],
                             d['instrumentalness'],
                             d['duration_ms'],
                             d['key'],
                             d['liveness'],
                             d['loudness'],
                             d['mode'],
                             d['valence'],
                             d['speechiness'],
                             d['tempo'],
                             d['time_signature'],
                             d['track_href'],
                             d['track_id'])

        cur.execute(sql_update_audio_, par_update_audio_)

    con.commit()
    con.close()
