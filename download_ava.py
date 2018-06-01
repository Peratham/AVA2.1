#!/usr/bin/python
import os
import urllib

# trainval vids
with open('./meta/ava_file_names_trainval_v2.1.txt','rb') as fp:
    vidlist = fp.readlines()
vidlist = [x.strip() for x in vidlist]

dummy_url = 'https://s3.amazonaws.com/ava-dataset/trainval/[file_name]'
print('[Info] Downloading trainval...')
for i, vidname in enumerate(vidlist, 1):
    dst = os.path.join('.', 'Data', 'trainval')
    if not os.path.exists(dst):
        os.makedirs(dst)
    vid_url = dummy_url.replace('[file_name]',vidname)
    print('[Info] Downloading {0}/{1}'.format(i,len(vidlist)))
    urllib.urlretrieve (vid_url, os.path.join(dst, "{}".format(vidname)))

# test vids
with open('./meta/ava_file_names_test_v2.1.txt','rb') as fp:
    vidlist = fp.readlines()
vidlist = [x.strip() for x in vidlist]

dummy_url = 'https://s3.amazonaws.com/ava-dataset/test/[file_name]'
print('[Info] Downloading test...')
for i, vidname in enumerate(vidlist, 1):
    dst = os.path.join('.', 'Data', 'test')
    if not os.path.exists(dst):
        os.makedirs(dst)
    vid_url = dummy_url.replace('[file_name]',vidname)
    print('[Info] Downloading {0}/{1}'.format(i,len(vidlist)))
    urllib.urlretrieve (vid_url, os.path.join(dst, "{}".format(vidname)))


