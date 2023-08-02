import sqlite3

con = sqlite3.connect("../MySpotifyData")
cur = con.cursor()

cur.execute("CREATE TABLE play("
            "id INTEGER PRIMARY KEY DESC, "
            "track_id TEXT, "
            "track_played_at TEXT, "
            "context TEXT "
            ")")

cur.execute("CREATE TABLE track("
            "id TEXT PRIMARY KEY, "
            "name TEXT, "
            "album_id TEXT, "
            "artist TEXT, "
            "duration_ms REAL, "
            "explicit INT, "
            "popularity INT, "
            "type TEXT, "
            "track_uri TEXT, "
            "first_played TEXT, "
            "last_played TEXT, "
            "times_played INT, "
            "is_saved INT "
            ")")

cur.execute("CREATE TABLE track_features("
            " track_id TEXT, "
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
