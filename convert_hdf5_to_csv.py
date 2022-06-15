import os
import glob
import hdf5_getters
import csv
import sys

file = open(sys.argv[2], 'w')
headers = [
    'title',
    'artist',
    'year',
    'location',
    'duration',
    'tempo',
    'loudness',
    'artist_hotness',
    'song_hotness'
]
writer = csv.DictWriter(file, fieldnames=headers, delimiter='|')
writer.writeheader()


def get_all_songs(basedir, ext='.h5'):
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*'+ext))
        for f in files:
            h5 = hdf5_getters.open_h5_file_read(f)

            title = hdf5_getters.get_title(h5).decode()
            artist = hdf5_getters.get_artist_name(h5).decode()
            year = hdf5_getters.get_year(h5)
            location = hdf5_getters.get_artist_location(h5).decode()
            duration = hdf5_getters.get_duration(h5)
            tempo = hdf5_getters.get_tempo(h5)
            loudness = hdf5_getters.get_loudness(h5)
            artist_hotness = hdf5_getters.get_artist_hotttnesss(h5)
            song_hotness = hdf5_getters.get_song_hotttnesss(h5)
            writer.writerow({
                'title': title,
                'artist': artist,
                'year': year,
                'location': location,
                'duration': duration,
                'tempo': tempo,
                'loudness': loudness,
                'artist_hotness': round(artist_hotness, 2),
                'song_hotness': round(song_hotness, 2)
            })

            h5.close()


get_all_songs(sys.argv[1])
file.close()
