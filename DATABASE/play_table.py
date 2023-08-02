import sqlite3

import settings


def insert_into_play(data):

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
        if not cur.fetchone():
            sql_insert_play_ = '''INSERT INTO play (track_id, track_played_at, context) 
                                  VALUES (?, ?, ?)'''
            par_insert_play_ = (d['track_id'], d['played_at'], d['context'])

            cur.execute(sql_insert_play_, par_insert_play_)

            # TRIGGER track TABLE
            # Search for the track in the track table
            sql_search_track_ = "SELECT name FROM track WHERE id = ? "
            par_search_track_ = [(d['track_id'])]

            cur.execute(sql_search_track_, par_search_track_)

            # IF the track is in the table already, we should update the last_played and times_played fields
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
