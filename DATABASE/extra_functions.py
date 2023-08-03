import sqlite3

import settings


def populate_track_table_from_play_table():
    # Select track_ids from play table and see what track_ids are not in the track table.

    # Open database connection
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    # Select track_ids and track_played_at from play table
    sql_select_track_ids_ = ''' SELECT track_id, track_played_at 
                                FROM play 
                                --WHERE track_played_at < '2023-08-02 18:38:06.482Z'
                                ORDER BY track_played_at ASC'''

    cur.execute(sql_select_track_ids_)
    aux_track = cur.fetchall()

    # Check if the tracks_ids are already in the track table
    for track in aux_track:
        sql_check_tracks_ids_in_track_table_ = ''' SELECT first_played, last_played, times_played
                                                   FROM track
                                                   WHERE id in (?)
                                                   ORDER BY first_played
                                                '''
        par_check_tracks_ids_in_track_table_ = [track[0]]

        cur.execute(sql_check_tracks_ids_in_track_table_, par_check_tracks_ids_in_track_table_)

        response = cur.fetchone()
        # If response is None or Null that means the track is not in the table and we should insert it
        if not response:
            sql_insert_track_ = '''INSERT INTO track (id, first_played, last_played, times_played) 
                                   VALUES (?, ?, ?, 1)'''
            par_insert_track_ = (track[0], track[1], track[1])

            cur.execute(sql_insert_track_, par_insert_track_)

        # The track is in the table, we should check if first_played,last_played should be updated and times_played + 1
        else:
            # What we have in the track table already
            r_firstplayed = response[0]
            r_lastplayed = response[1]
            r_timesplayed = response[2]

            # What we have in the play table
            track_id = track[0]
            track_played_at = track[1]

            # new track_played at is BEFORE the first_played
            if track_played_at < r_firstplayed:
                update_first_played = track_played_at
                update_last_played = r_lastplayed

            # new track_played is AFTER the last_played
            elif r_lastplayed < track_played_at:
                update_first_played = r_firstplayed
                update_last_played = track_played_at

            else:
                update_first_played = r_firstplayed
                update_last_played = r_lastplayed

            r_timesplayed = r_timesplayed + 1

            sql_update_track_ = ''' UPDATE track 
                                    SET first_played = ?, last_played = ?, times_played = ?
                                    WHERE id = ? '''
            par_update_track_ = (update_first_played, update_last_played, r_timesplayed, track_id)

            cur.execute(sql_update_track_, par_update_track_)

    con.commit()

    con.close()


populate_track_table_from_play_table()
