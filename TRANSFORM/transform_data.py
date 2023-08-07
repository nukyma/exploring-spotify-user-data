def recently_played_tracks_response(data):
    """
    get as much data as possible from the response to get_user_recently_played_tracks
    :param data: response
    :return:
    """

    # played_tracks for PLAY table
    played_tracks = list()
    map_track_album_info = list()
    map_track_artist_info = list()
    for i in data['items']:
        played_tracks.append({'track_id': i['track']['id'],
                              'played_at': i['played_at'].replace('T', ' '),
                              'context': i['context']['type']}
                             )

        map_track_album_info.append({
            'track_id': i['track']['id'],
            'album_id': i['track']['album']['id'],
            'played_at': i['played_at'].replace('T', ' '),
            'context': i['context']['type'],
        })

        for k in i['track']['artists']:
            map_track_artist_info.append({'track_id': i['track']['id'],
                                          'artist_id': k['id'],
                                          'played_at': i['played_at'].replace('T', ' '),
                                          'context': i['context']['type']
                                          })

    # track_info for TRACK table
    track_info = list()
    for j in data['items']:

        artists_id = list()
        artists_names = list()
        for m in j['track']['artists']:
            artists_id.append(m['id'])
            artists_names.append(m['name'])

        track_info.append({'id': j['track']['id'],
                           'name': j['track']['name'],
                           'album_id': j['track']['album']['id'],
                           'album_name': j['track']['album']['name'],
                           'artists_id': str(artists_id),
                           'artists_names': str(artists_names),
                           'duration_ms': j['track']['duration_ms'],
                           'explicit': j['track']['explicit'],
                           'type': j['track']['type'],
                           'preview_url': j['track']['external_urls']['spotify']
                           })

    return played_tracks, track_info, map_track_album_info, map_track_artist_info


def make_batches_of_tracks_ids(size, data):
    # batch_ids expected format: "7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B"

    list_batches = list()
    counter = 0
    string_ids = ""
    for i in data:
        if counter <= size - 1 and i != data[len(data) - 1]:
            string_ids = string_ids + str(i) + ','
            counter += 1

        elif counter == size and i != data[len(data) - 1]:

            # Clean the ' chars
            string_ids = string_ids.replace("'", "")
            # Get rid of the last comma
            string_ids = string_ids[:-1]

            list_batches.append(string_ids)

            counter = 0
            string_ids = ""

        elif i == data[len(data) - 1]:
            # Clean the ' chars
            string_ids = string_ids.replace("'", "")
            # Get rid of the last comma
            string_ids = string_ids[:-1]

            list_batches.append(string_ids)

    return list_batches


def tracks_info(data):
    insert_list = list()
    for d in data:
        if 'tracks' in d.keys():
            for i in d['tracks']:

                artists_id = list()
                artists_names = list()
                for a in i['artists']:
                    artists_id.append(a['id'])
                    artists_names.append(a['name'])

                track = {'id': i['id'],
                         'name': i['name'],
                         'album_id': i['album']['id'],
                         'album_name': i['album']['name'],
                         'artists_id': str(artists_id),
                         'artists_names': str(artists_names),
                         'duration_ms': i['duration_ms'],
                         'explicit': i['explicit'],
                         'type': i['type'],
                         'preview_url': i['preview_url']
                         }

                insert_list.append(track)

    return insert_list


def audio_features_info(data):
    insert_list = list()
    for d in data:
        if 'audio_features' in d.keys():
            for i in d['audio_features']:
                if i:
                    audio_feature = {'track_id': i['id'],
                                     'acousticness': i['acousticness'],
                                     'analysis_url': i['analysis_url'],
                                     'danceability': i['danceability'],
                                     'duration_ms': i['duration_ms'],
                                     'energy': i['energy'],
                                     'instrumentalness': i['instrumentalness'],
                                     'key': i['key'],
                                     'liveness': i['liveness'],
                                     'loudness': i['loudness'],
                                     'mode': i['mode'],
                                     'valence': i['valence'],
                                     'speechiness': i['speechiness'],
                                     'tempo': i['tempo'],
                                     'time_signature': i['time_signature'],
                                     'track_href': i['track_href']}

                    insert_list.append(audio_feature)

    return insert_list


def artist_info(data):
    """
    Get response artist data and format it for posterior load in database
    :param data: response endpoint data
    :return: artist info formatted and ready to be loaded in DB
    """
    insert_list = list()
    for d in data:
        if 'artists' in d.keys():
            for i in d['artists']:
                if i:
                    artist = {'id': i['id'],
                              'name': i['name'],
                              'genres': str(i['genres']),
                              'followers': i['followers']['total'],
                              'external_urls': i['external_urls']['spotify']
                              }

                    insert_list.append(artist)

    return insert_list


def album_info(data):
    """
    Get response album data and format it for posterior load in database
    :param data: response endpoint data
    :return: album info formatted and ready to be loaded in DB
    """
    insert_list = list()
    for d in data:
        if 'albums' in d.keys():
            for i in d['albums']:
                if i:
                    # Artists lists
                    artists_ids = list()
                    artists_names = list()
                    for j in i['artists']:
                        artists_ids.append(j['id'])
                        artists_names.append(j['name'])

                    album = {'id': i['id'],
                             'name': i['name'],
                             'genres': str(i['genres']),
                             'album_type': i['album_type'],
                             'total_tracks': i['total_tracks'],
                             'release_date': i['release_date'],
                             'label': i['label'],
                             'artist_album_name': str(artists_names),
                             'artist_album_id': str(artists_ids),
                             'external_urls': i['external_urls']['spotify']
                             }

                    insert_list.append(album)

    return insert_list
