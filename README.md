# MetOpenAccessDownloader
For the purpose of creating a dataset of artworks, I created this python script to download all public images from the MET Museum through their API.

You can use it like this: ```python downloadDataset.py -o datasets/ -t artists.txt``` if you have a text called artists with a artist or culture per line and want to create a datasets folder for the output. Or you can use ```python downloadDataset.py -o datasets/ -n "Vincent van Gogh"``` if you only want to get all images from one artist.
