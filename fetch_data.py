import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Ambil kunci dari GitHub Secrets
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# Sambung ke Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Senarai Artis Nasyid Malaysia yang nak ditarik
ARTISTS = {
    'Raihan': '2893j4VvWwX9H08nE72qT5',
    'Rabbani': '6y4L1S5V8C3GZ4QxJ8a9bC',
    'Hijjaz': '1x1G0R8K8S9T7U0V1W2X3Y'
}

data_list = []

print("Mula menarik data dari Spotify...")

for artist_name, artist_id in ARTISTS.items():
    try:
        # Tarik album-album artis
        albums = sp.artist_albums(artist_id, album_type='album')
        
        for album in albums['items']:
            album_id = album['id']
            album_detail = sp.album(album_id)
            
            release_date = album_detail.get('release_date', 'N/A')
            year = release_date[:4] if release_date else 'N/A'
            label = album_detail.get('label', 'N/A')
            
            # Tarik lagu dalam album
            tracks = sp.album_tracks(album_id)
            for track in tracks['items']:
                track_info = sp.track(track['id'])
                
                data_list.append({
                    'Nama Artis': artist_name,
                    'Tajuk Album': album['name'],
                    'Tajuk Lagu': track['name'],
                    'Tahun Terbitan': year,
                    'Label': label,
                    'Skor Populariti (0-100)': track_info.get('popularity', 0),
                    'Spotify URL': track['external_urls']['spotify']
                })
    except Exception as e:
        print(f"Ralat pada artis {artist_name}: {e}")

# Tukar data jadi fail CSV
df = pd.DataFrame(data_list)
df.to_csv('munsyid_data.csv', index=False)
print("Data berjaya disimpan dalam fail munsyid_data.csv!")
