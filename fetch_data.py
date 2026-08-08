import requests
import pandas as pd

# Kau boleh tambah nama kumpulan lain dalam kurungan ini nanti!
ARTISTS = ['Raihan', 'Rabbani', 'Hijjaz', 'Inteam', 'UNIC'] 
data_list = []

print("Mula menarik data dari pelayan Apple Music...")

for artist in ARTISTS:
    print(f"Sedang mencari data untuk: {artist}")
    # URL carian iTunes API (country=MY untuk pasaran Malaysia)
    url = f"https://itunes.apple.com/search?term={artist}&entity=song&limit=200&country=my"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'results' in data:
            for track in data['results']:
                # Pastikan nama artis betul (elak tarik lagu artis lain nama sama)
                if artist.lower() in track.get('artistName', '').lower():
                    release_date = track.get('releaseDate', 'N/A')
                    year = release_date[:4] if release_date != 'N/A' else 'N/A'
                    
                    data_list.append({
                        'Nama Artis': track.get('artistName', 'N/A'),
                        'Tajuk Album': track.get('collectionName', 'N/A'),
                        'Tajuk Lagu': track.get('trackName', 'N/A'),
                        'Tahun Terbitan': year,
                        'Genre': track.get('primaryGenreName', 'N/A'),
                        'Pautan': track.get('trackViewUrl', '#')
                    })
    except Exception as e:
        print(f"Ralat pada artis {artist}: {e}")

# Tukar data jadi jadual
df = pd.DataFrame(data_list)

# Buang lagu yang berulang (duplicate)
df = df.drop_duplicates(subset=['Tajuk Lagu', 'Nama Artis'])

# Simpan ke CSV
df.to_csv('munsyid_data.csv', index=False)
print(f"Berjaya! {len(df)} lagu telah berjaya disimpan ke dalam munsyid_data.csv")
