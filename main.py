import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from prettytable import PrettyTable
import pandas as pd
import config


client_credentials_manager = SpotifyClientCredentials(
    client_id=config.SPOTIPY_CLIENT_ID,
    client_secret=config.SPOTIPY_CLIENT_SECRET
)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Top 10 Tracks for given Artist
artist_name = "Lil Baby"
results = spotify.search(q=f"artist:{artist_name}", type="artist")
artist = results["artists"]["items"][0]
top_tracks = spotify.artist_top_tracks(artist["id"])
for track in top_tracks["tracks"]:
    print(track["name"])


# Define a function to get the top tracks for a given time range
def get_top_tracks(time_range):
    if time_range == "week":
        results = spotify.playlist("37i9dQZEVXbMDoHDwVN2tF")  # Top 50 Global (last 7 days)
    elif time_range == "month":
        results = spotify.playlist("37i9dQZEVXbJiZcmkrIHGU")  # Top 50 Global (last 4 weeks)
    elif time_range == "year":
        results = spotify.playlist("37i9dQZEVXbLRQDuF5jeBp")  # Top 100 Global (last 12 months)
    else:
        return []

    tracks = []
    for track in results["tracks"]["items"]:
        tracks.append({
            "name": track["track"]["name"],
            "artist": track["track"]["artists"][0]["name"],
            "album": track["track"]["album"]["name"],
            "release_date": track["track"]["album"]["release_date"],
            "image_url": track["track"]["album"]["images"][0]["url"],
            "preview_url": track["track"]["preview_url"],
            "spotify_url": track["track"]["external_urls"]["spotify"]
        })

    return tracks[:10]  # Return the top 10 tracks

# Get the top tracks for the week, month, and year
top_tracks_week = get_top_tracks("week")
top_tracks_month = get_top_tracks("month")
top_tracks_year = get_top_tracks("year")

# Create a table for the top tracks of the week
table_week = PrettyTable()
table_week.field_names = ["Rank", "Name", "Artist", "Album", "Release Date", "Preview URL"]

# Add the top tracks for the week to the table
for i, track in enumerate(top_tracks_week):
    table_week.add_row([i+1, track["name"], track["artist"], track["album"], track["release_date"], track["preview_url"]])

# Create a table for the top tracks of the month
table_month = PrettyTable()
table_month.field_names = ["Rank", "Name", "Artist", "Album", "Release Date", "Preview URL"]

# Add the top tracks for the month to the table
for i, track in enumerate(top_tracks_month):
    table_month.add_row([i+1, track["name"], track["artist"], track["album"], track["release_date"], track["preview_url"]])

# Create a table for the top tracks of the year
table_year = PrettyTable()
table_year.field_names = ["Rank", "Name", "Artist", "Album", "Release Date", "Preview URL"]

# Add the top tracks for the year to the table
for i, track in enumerate(top_tracks_year):
    table_year.add_row([i+1, track["name"], track["artist"], track["album"], track["release_date"], track["preview_url"]])

# Print out the tables of top tracks
print("Top 10 tracks of the week:")
print(table_week)

# Convert the top tracks data into pandas dataframes
df_week = pd.DataFrame(top_tracks_week)
df_month = pd.DataFrame(top_tracks_month)
df_year = pd.DataFrame(top_tracks_year)

# Export the dataframes to CSV files
df_week.to_csv("top_tracks_week.csv", index=False)
df_month.to_csv("top_tracks_month.csv", index=False)
df_year.to_csv("top_tracks_year.csv", index=False)