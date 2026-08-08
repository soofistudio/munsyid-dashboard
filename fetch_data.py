import requests
import pandas as pd

ARTISTS = ['Raihan', 'Rabbani', 'Hijjaz', 'Inteam', 'UNIC', 'A.N.A The Rayhan', 'AEYDAN', 'Azwan Far East', 'Adikku Sayang', 'Ae-man', 'Akhil Hayy', 'Ae-One', 'Alarm Me', 'Al-Faradis', 'Aliff Ila Ya', 'Anugerah', 'Ustaz Amal', 'AMAR', 'The Bangsar Boyz and Friends', 'Bazli Unic', 'Darwish', 'Devotees', 'Diwani', 'RAST', 'ARDANI', 'Major 9', 'Soofi All Stars', 'Daqmie', 'Far East', 'Saujana', 'Mirwana', 'Nowseeheart', 'Fitri Haris', 'Fadzli Far East', 'Zayne', 'Rabithah', 'One Path', 'Adnin Roslan', 'Halim Ahmad', 'Saujana', 'Zawfan', 'Zayne', 'Marhaen', 'In-Team', 'Instinct', 'Amer BinYusoff', 'Fathi Saleem', 'Munif Hijjaz', 'Mestica', 'Dehearty', 'Anas Tahir', 'Syahrul Asad', 'Ustaz 3 Beradik', 'Maliq Suhaimi', 'Saff One', 'Simfoni', 'Imtiaz Simfoni', 'Munif Ahmad', 'Isman Hijjaz', 'The Muhibbain', 'Nazrey Johani', 'The Zikr', 'UMNAA', 'Amirul Zahid', 'Arsy Osman', 'Naufal Syakirin', 'Intisor', 'Wildaniey', 'Andika', 'Autotune Band', 'The Truth', 'Aniq Muhai', 'Fetya', 'Syed Salahuddin', 'Aftermath', 'GAU NASHEED'] 
data_list = []

for artist in ARTISTS:
    url = f"https://itunes.apple.com/search?term={artist}&entity=song&limit=200&country=my"
    try:
        response = requests.get(url)
        data = response.json()
        if 'results' in data:
            for track in data['results']:
                if artist.lower() in track.get('artistName', '').lower():
                    # Tukar 100x100 ke 600x600 untuk kualiti HD
                    cover_url = track.get('artworkUrl100', '').replace('100x100bb', '600x600bb')
                    data_list.append({
                        'id': track.get('trackId'),
                        'Nama Artis': track.get('artistName'),
                        'Tajuk Album': track.get('collectionName'),
                        'Tajuk Lagu': track.get('trackName'),
                        'Tahun': track.get('releaseDate')[:4],
                        'Genre': track.get('primaryGenreName'),
                        'Pautan': track.get('trackViewUrl'),
                        'Cover': cover_url
                    })
    except Exception as e: print(f"Error {artist}: {e}")

df = pd.DataFrame(data_list).drop_duplicates(subset=['id'])
df.to_csv('munsyid_data.csv', index=False)
