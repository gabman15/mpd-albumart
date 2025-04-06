from mpd import MPDClient
import time
import argparse

album_file = "/tmp/album.png"

def dl_album(client, song):
    try:
        img = client.readpicture(song)['binary']
        f = open(album_file,'wb')
        f.write(img)
        f.close()
    except:
        try:
            img = client.albumart(song)['binary']
            f = open(album_file,'wb')
            f.write(img)
            f.close()
        except:
            print("Failed to get album cover")

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(prog='mpd-albumart')
    parser.add_argument('--host', default="localhost")
    args = parser.parse_args()
    mpd_host = args.host

    client = MPDClient()
    curr_song = {}

    try:
        client.connect(mpd_host,6600)
        curr_song = client.currentsong()
        if curr_song:
            dl_album(client, curr_song['file'])
        client.close()
        client.disconnect()
    except:
        print("Couldn't connect to mpd. Retrying...")
        time.sleep(5)

    while (True):
        try:
            client.connect(mpd_host,6600)
            new_song = client.currentsong()
            if new_song:
                if (new_song != curr_song):
                    curr_song = new_song
                    dl_album(client, curr_song['file'])
            client.disconnect()
            time.sleep(2)
        except:
            print("Couldn't connect to mpd. Retrying...")
            time.sleep(5)
