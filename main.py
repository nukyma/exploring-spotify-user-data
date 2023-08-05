from API import extract_data, connection
from DATABASE import play_table, track_table, audio_features_table
from TRANSFORM import transform_data

if __name__ == '__main__':

    spotify, token = connection.connect_spotify_api()

    # Use own methods to pull raw data from the Spotify API
    # user_info = extract_data.get_user_private_info(sp=spotify)

    ###         USER LAST 50 PLAYED SONGS                       ###
    # Extract
    played_tracks = extract_data.get_user_recently_played_tracks(sp=spotify)
    # Transform: Select, clean and transform data
    played_tracks_dict = transform_data.recently_played_tracks(data=played_tracks)
    # Load
    play_table.insert_into_play(data=played_tracks_dict)

    ###         COMPLETE TRACKS INFO IN BATCHES OF 50           ###
    # Consult our DB
    list_tracks_ids = track_table.get_tracks_incomplete()
    # BATCH
    list_batch_ids = transform_data.make_batches_of_tracks_ids(size=50, data=list_tracks_ids)
    # Extract
    info_tracks = list()
    for i in list_batch_ids:
        info_tracks.append(extract_data.get_several_tracks_info(sp=spotify, batch_ids=i))
    # Transform
    info_tracks_dict = transform_data.tracks_info(data=info_tracks)
    # Load
    track_table.insert_into_track(data=info_tracks_dict)

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
