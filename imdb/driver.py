__author__ = 'vamshi'

import os
import sys
from imdb_file_downloader import ImdbFileDownloadManager
from imdb_file_loader import ImdbMovieDataLoader

IMDB_DATA_FOLDER = 'imdb_files'

if __name__ == "__main__":
    output_folder = os.path.join('/'.join(sys.argv[0].split('/')[:-1]), IMDB_DATA_FOLDER)
    #ImdbFileDownloadManager(1,output_folder).begin_downloads()
    loader = ImdbMovieDataLoader(output_folder)
    loader.load_mongodb_bulk('localhost', 27017, 'imdb', 'movies')

