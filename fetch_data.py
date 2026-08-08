import requests
import pandas as pd

# Kau boleh tambah nama kumpulan lain dalam kurungan ini nanti!
ARTISTS = ['Raihan', 'Rabbani', 'Hijjaz', 'Inteam', 'UNIC', 'A.N.A The Rayhan', 'AEYDAN', 'Azwan Far East', 'Adikku Sayang', 'Ae-man', 'Akhil Hayy', 'Ae-One', 'Alarm Me', 'Al-Faradis', 'Aliff Ila Ya', 'Anugerah', 'Ustaz Amal', 'AMAR', 'The Bangsar Boyz and Friends', 'Bazli Unic', 'Darwish', 'Devotees', 'Diwani', 'RAST', 'ARDANI', 'Major 9', 'Soofi All Stars', 'Daqmie', 'Far East', 'Saujana', 'Mirwana', 'Nowseeheart', 'Fitri Haris', 'Fadzli Far East', 'Zayne', 'Rabithah', 'One Path', 'Adnin Roslan', 'Halim Ahmad', 'Saujana', 'Zawfan', 'Zayne', 'Marhaen', 'In-Team', 'Instinct', 'Amer BinYusoff', 'Fathi Saleem', 'Munif Hijjaz', 'Mestica', 'Dehearty', 'Anas Tahir', 'Syahrul Asad', 'Ustaz 3 Beradik', 'Maliq Suhaimi', 'Saff One', 'Simfoni', 'Imtiaz Simfoni', 'Munif Ahmad', 'Isman Hijjaz', 'The Muhibbain', 'Nazrey Johani', 'The Zikr', 'UMNAA', 'Amirul Zahid', 'Arsy Osman', 'Naufal Syakirin', 'Intisor', 'Wildaniey', 'Andika', 'Autotune Band', 'The Truth', 'Aniq Muhai', 'Fetya', 'Syed Salahuddin', 'Aftermath', 'GAU NASHEED'] 
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
