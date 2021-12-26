import os
import requests
import urllib.request
import argparse
import string
import urllib.parse
from requests.utils import requote_uri

def download_met(artist):
    try:
        url = "https://collectionapi.metmuseum.org/public/collection/v1/search?" \
              f"hasImage=true&artistOrCulture=true&q={artist.replace(' ', '%20')}"

        print(url)

        r = requests.get(url=url)

        data = r.json()

    except ConnectionError:
        print(ConnectionError.strerror)
        return

    print(data)

    if not data['objectIDs']:
        print("No Result found")
        return

    try:
        out_dir = os.path.join(args.out, artist)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

    except IOError:
        print(IOError.strerror)
        return

    for oid in data['objectIDs']:
        try:
            url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}"

            r = requests.get(url=url)

            id_data = r.json()
            filename = sanitize(f"{id_data['artistDisplayName']}_{id_data['title']}.jpg")
            picurl = requote_uri(id_data['primaryImage'])
            print("picture URL:"+picurl)
            urllib.request.urlretrieve(picurl,
                                       os.path.join(out_dir, filename))
        except ConnectionError:
            print(ConnectionError.strerror)


def sanitize(dirty_string):
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    clean_string = ''.join(char for char in dirty_string if char in valid_chars)
    clean_string = clean_string.replace(' ', '_')
    return clean_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    input_group = parser.add_argument_group("input")
    input_group.add_argument("-n", "--name", help="name of a culture or an artist")
    input_group.add_argument("-t", "--text", help="file with one culture or artist per line")
    parser.add_argument("-o", "--out", help="directory where the pictures shall be stored")
    args = parser.parse_args()

    if args.text:
        f = open(args.text, "r")
        for line in f:
            print(line)
            download_met(sanitize(line))
        f.close()

    else:
        download_met(args.name)

