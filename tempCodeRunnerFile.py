artist_name = "Drake"
results = spotify.search(q=f"artist:{artist_name}", type="artist")
artist = results["artists"]["items"][0]
top_tracks = spotify.artist_top_tracks(artist["id"])
for track in top_tracks["tracks"]:
    print(track["name"])