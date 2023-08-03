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


def make_batches_of_tracks_ids(size, data):
    list_batches = list()
    counter = 0
    string_ids = ""
    for i in data:

        if counter <= size - 1:
            string_ids = string_ids + str(i) + ','
            counter += 1
        else:
            # batch_ids expected format: "7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B"
            # Clean the ' at start and end of every id
            string_ids = string_ids.replace("'", "")
            # Include the first ' char
            string_ids = "'" + string_ids
            # Get rid of the last comma and add the last ' char
            string_ids = string_ids[:-1] + "'"

            list_batches.append(string_ids)

            counter = 0
            string_ids = ""

    return list_batches
