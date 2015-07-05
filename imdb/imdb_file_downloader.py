__author__ = 'vamshi'

import urllib2
import os
import sys
import zlib
import Queue
from threading import Thread

IMDB_FTP_URL = "ftp://ftp.fu-berlin.de/pub/misc/movies/database"

DB_FILES = [
    'ratings.list',
    'movies.list',
    'genres.list',
    'directors.list',
    'actors.list',
    'actresses.list',
    'running-times.list',
    'language.list'
]

class Downloader(Thread):
    def __init__(self, queue, output_directory):
        Thread.__init__(self)
        self.queue = queue
        self.output_directory = output_directory

    def run(self):
        while True:
            url, df = self.queue.get()
            try:
                self.download_unzip(url, df)
            except:
                pass
            self.queue.task_done()

    def download_unzip(self, url, local_filename):
        fn = os.path.join(self.output_directory, local_filename)
        resp = urllib2.urlopen(url)
        CHUNK = 8 * 1024
        d = zlib.decompressobj(16+zlib.MAX_WBITS) #this magic number can be inferred from the structure of a gzip file
        with open(fn, 'wb') as fp:
            while True:
                data = resp.read(CHUNK)
                if not data: break
                data = d.decompress(data)
                fp.write(data)
                fp.flush()
        return

class ImdbFileDownloadManager:
    def __init__(self, thread_count, output_directory):
        self.q = Queue.Queue()
        self.thread_count = thread_count
        self.output_directory = output_directory

    def begin_downloads(self):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        for i in range(self.thread_count):
            t = Downloader(self.q, self.output_directory)
            t.setDaemon(True)
            t.start()
        for df in DB_FILES:
            self.q.put((os.path.join(IMDB_FTP_URL, df + '.gz'),df))
        self.q.join()
        return

