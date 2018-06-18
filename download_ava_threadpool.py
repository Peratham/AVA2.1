#!/usr/bin/python
import os
import urllib
from multiprocessing.pool import ThreadPool
import zipfile

# download annotation zipfile and extract
dst = os.path.join('.', 'meta')
if not os.path.exists(dst):
	os.makedirs(dst)
anno_url = 'https://s3.amazonaws.com/ava-dataset/annotations/ava_v2.1.zip'
urllib.urlretrieve (anno_url, os.path.join(dst, 'ava_v2.1.zip'))

zip_ref = zipfile.ZipFile(os.path.join(dst, 'ava_v2.1.zip'), 'r')
zip_ref.extractall(dst)
zip_ref.close()

# trainval/test filenames
tfilename_url = 'https://s3.amazonaws.com/ava-dataset/annotations/ava_file_names_trainval_v2.1.txt'
urllib.urlretrieve (tfilename_url, os.path.join(dst, 'ava_file_names_trainval_v2.1.txt'))
tfilename_url = 'https://s3.amazonaws.com/ava-dataset/annotations/ava_file_names_test_v2.1.txt'
urllib.urlretrieve (tfilename_url, os.path.join(dst, 'ava_file_names_test_v2.1.txt'))

from time import time as timer

def fetch_url(vid_url_tuple):
	url, dst, vidname = vid_url_tuple
	try:
		# print('[Info] Downloading '.format(vidname))
		urllib.urlretrieve (url, os.path.join(dst, vidname))
		return url, None
	except Exception as e:
		return url, e

# trainval vids
dst = os.path.join('.', 'Data', 'trainval')
if not os.path.exists(dst):
	os.makedirs(dst)

with open('./meta/ava_file_names_trainval_v2.1.txt','rb') as fp:
	vidlist = fp.readlines()
vidlist = [x.strip() for x in vidlist]
dummy_url = 'https://s3.amazonaws.com/ava-dataset/trainval/[file_name]'
vid_urls = [(dummy_url.replace('[file_name]',vidname), dst, vidname) for vidname in vidlist]

print('[Info] Downloading trainval...')
start = timer()
results = ThreadPool(20).imap_unordered(fetch_url, vid_urls)
for url, error in results:
	if error is None:
		print("%r fetched in %ss" % (url, timer() - start))
	else:
		print("error fetching %r: %s" % (url, error))

print("Elapsed Time: %ss" % (timer() - start,))

# test vids
dst = os.path.join('.', 'Data', 'test')
if not os.path.exists(dst):
	os.makedirs(dst)

with open('./meta/ava_file_names_test_v2.1.txt','rb') as fp:
	vidlist = fp.readlines()
vidlist = [x.strip() for x in vidlist]
dummy_url = 'https://s3.amazonaws.com/ava-dataset/test/[file_name]'
vid_urls = [(dummy_url.replace('[file_name]',vidname), dst, vidname) for vidname in vidlist]

print('[Info] Downloading test...')
start = timer()
results = ThreadPool(20).imap_unordered(fetch_url, vid_urls)
for url, error in results:
	if error is None:
		print("%r fetched in %ss" % (url, timer() - start))
	else:
		print("error fetching %r: %s" % (url, error))

print("Elapsed Time: %ss" % (timer() - start,))
