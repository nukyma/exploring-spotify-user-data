import sqlite3

import settings


def create_play_table():
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    cur.execute("CREATE TABLE play("
                "track_id TEXT , "
                "track_played_at TEXT , "
                "context TEXT ,"
                "PRIMARY KEY (track_id, track_played_at)"
                ")")
    con.commit()
    con.close()


def create_track_table():
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    cur.execute("CREATE TABLE track("
                "id TEXT PRIMARY KEY, "
                "name TEXT, "
                "album_id TEXT, "
                "album_name TEXT, "
                "artists_id TEXT, "
                "artists_names TEXT, "
                "duration_ms REAL, "
                "explicit INT, "
                "type TEXT, "
                "track_uri TEXT, "
                "first_played TEXT, "
                "last_played TEXT, "
                "times_played INT, "
                "is_saved INT "
                ")")

    con.commit()
    con.close()


def create_audio_features_table():
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    cur.execute("CREATE TABLE audio_features("
                "track_id TEXT PRIMARY KEY, "
                "acousticness REAL, "
                "analysis_url TEXT, "
                "danceability REAL, "
                "duration_ms INT, "
                "energy REAL, "
                "instrumentalness REAL, "
                "key INT, "
                "liveness REAL, "
                "loudness REAL, "
                "mode INT, "
                "valence REAL,  "
                "speechiness REAL, "
                "tempo REAL, "
                "time_signature INT, "
                "track_href TEXT "
                ")")

    con.commit()
    con.close()


def create_album_table():
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    cur.execute("CREATE TABLE album("
                "id TEXT PRIMARY KEY, "
                "name TEXT,"
                "genres TEXT,"
                "album_type TEXT, "
                "total_tracks INT, "
                "external_urls TEXT,"
                "release_date TEXT,"
                "label TEXT,"
                "artist_album_name TEXT,"
                "artist_album_id TEXT,"
                "first_played TEXT,"
                "last_played TEXT,"
                "is_user_saved INT"
                ")")

    con.commit()
    con.close()


def create_artist_table():
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    cur.execute("CREATE TABLE artist("
                "id TEXT PRIMARY KEY, "
                "name TEXT,"
                "genres TEXT,"
                "followers INT,"
                "external_urls TEXT,"
                "first_played TEXT,"
                "last_played TEXT,"
                "is_user_saved INT"
                ")")

    con.commit()
    con.close()


def create_map_track_album_table():
    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    cur.execute("CREATE TABLE map_track_album("
                "track_id TEXT , "
                "album_id TEXT , "
                "played_at TEXT , "
                "context TEXT ,"
                "PRIMARY KEY (track_id, album_id)"
                ")")
    con.commit()
    con.close()


def create_map_track_artist_table():

    con = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    cur = con.cursor()

    cur.execute("CREATE TABLE map_track_artist("
                "track_id TEXT , "
                "artist_id TEXT , "
                "played_at TEXT , "
                "context TEXT ,"
                "PRIMARY KEY (track_id, artist_id)"
                ")")
    con.commit()
    con.close()

