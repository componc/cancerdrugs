'''
Helper functions
'''

import logging, os, csv, gzip, json, mimetypes, hashlib, zipfile, glob, re, time
from datetime import datetime, timedelta
import concurrent.futures, os, urllib.request, shutil
import xml.etree.ElementTree as ET
import pandas as pd


def normalize(s):
    '''Normalize string by replacing all spaces with underscores and removing all non-word characters.'''
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def snake_to_camel(s):
    '''Convert snake to camel case.'''
    parts = s.split('_')
    return parts[0] + ''.join(part.capitalize() for part in parts[1:])


def hash_url(url):
    '''Create SHA256 hash from url.'''
    return hashlib.sha256(url.lower().encode('utf-8')).hexdigest()


def download_file(url, filename=None, path=os.getcwd(), blocksize=4096, overwrite=False, max_age=timedelta.max):
    filepath = os.path.join(path, filename)
    try:
        # Check if file already exists
        if (os.path.exists(filepath) and
            not overwrite and
            datetime.now() - datetime.fromtimestamp(os.path.getmtime(filepath)) <= max_age):
            sha256_hash = hashlib.sha256()
            size = 0
            with open(filepath, 'rb') as f:
                for block in iter(lambda: f.read(blocksize), b''):
                    size += len(block)
                    sha256_hash.update(block)
            logging.info(f'The specified file {filepath} already exists ({size} bytes, SHA256 {sha256_hash.hexdigest()}).')
            return (filepath, size, sha256_hash.hexdigest())
        # If not download
        with urllib.request.urlopen(url) as res:
            if not filename:
                filename = res.info().get_filename()
            sha256_hash = hashlib.sha256()
            size = 0
            with open(filepath, 'wb') as f:
                for block in iter(lambda: res.read(blocksize), b''):
                    size += len(block)
                    sha256_hash.update(block)
                    f.write(block)
            logging.info(f'Successfully downloaded file from {url} to {filepath} ({size} bytes, SHA256 {sha256_hash.hexdigest()}).')
            return (filepath, res.length, sha256_hash.hexdigest())
    except:
        logging.error(f'Error retrieving file from {url}.')
        return None


def get_json(url, cache_dir=os.getcwd(), max_age=timedelta.max, overwrite=False):
    url_hash = hash_url(url)
    filepath = os.path.join(cache_dir, url_hash + '.json')
    # Check if cached
    try:
        if (os.path.exists(filepath) and
            not overwrite and
            datetime.now() - datetime.fromtimestamp(os.path.getmtime(filepath)) <= max_age):
            data = open(filepath, 'rb').read()
            obj = json.loads(data)
            sha256_hash = hashlib.sha256(data).hexdigest()
            logging.info(f'Successfully retrieved JSON object from cache ({len(data)} bytes, SHA256 {sha256_hash}).')
            return obj
        # Download JSON from url
        with urllib.request.urlopen(url) as res:
            data = res.read()
            sha256_hash = hashlib.sha256(data)
            obj = json.loads(data)
        if obj and cache_dir:
            open(filepath, 'wb').write(data) #json.dumps(obj, indent=2, sort_keys=True, default=str)
        logging.info(f'Successfully retrieved JSON object from {url} ({len(data)} bytes, SHA256 {sha256_hash.hexdigest()}).')
        return obj
    except:
        logging.error(f'Error retrieving JSON object from {url}.')
        return None
    

def create_archive(filename, path, pattern='**/*', recursive=True):
    '''Create zip archive and add all files specified by path and pattern.'''
    try:
        with zipfile.ZipFile(filename, 'w') as zf:
            for file in glob.iglob(os.path.join(path, pattern), recursive=recursive):
                relpath = os.path.relpath(file, path)
                zf.write(file, arcname=relpath)
        logging.info(f'Successfully created archive {filename}.')
    except:
        logging.error(f'Error creating archive {filename}.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    '''# Test download_file
    test_url = 'https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Chemical/19894120/JSON/'
    download_file(test_url, 'test.json', max_age=timedelta(seconds=5), overwrite=True)
    download_file(test_url, 'test.json', max_age=timedelta(seconds=5))
    logging.info('Sleeping 10 seconds...')
    time.sleep(10)
    download_file(test_url, 'test.json', max_age=timedelta(seconds=10))
    # Test get_json
    test_url = 'https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Chemical/19894120/JSON/'
    get_json(test_url, max_age=timedelta(seconds=5), overwrite=True)
    get_json(test_url, max_age=timedelta(seconds=5))
    logging.info('Sleeping 10 seconds...')
    time.sleep(10)
    get_json(test_url, max_age=timedelta(seconds=10))'''
    pass
