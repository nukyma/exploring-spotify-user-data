def recently_played_tracks(data):
    played_tracks = list()
    for i in data['items']:
        track_id = i['track']['id']
        played_at = i['played_at'].replace('T', ' ')
        context = i['context']['type']

        played_tracks.append({'track_id': track_id,
                              'played_at': played_at,
                              'context': context}
                             )

    return played_tracks
