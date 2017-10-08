import os
import json
import hashlib


def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def getsubs(dir):
    # get all

    dirs = []
    # files = []
    index = {}
    diff = {}

    def update_index(filepath, hash, size):
        if hash in index:
            index[hash].append([size, filepath])
            diff.update({hash: index[hash]})
        else:
            index.update({hash: [[size, filepath]]})

    for dirname, dirnames, filenames in os.walk(dir):

        dirs.append(dirname)

        for subdirname in dirnames:
            dirs.append(os.path.join(dirname, subdirname))

        for filename in filenames:
            # files.append(os.path.join(dirname, filename))
            fullpath = os.path.join(dirname, filename)
            try:
                size = os.path.getsize(fullpath)
            except OSError:
                pass
            else:
                update_index(fullpath, hashfile(fullpath), size)

    return diff

d = getsubs("/Users/cold00n/SAMPLES/")

"""
with open(filename, 'wb') as outfile:
    json.dump(data, outfile)
with open(filename) as infile:
    data = json.load(infile)
"""




"""
1.)calc size profit after removing!!!

implement removing algorithm:
1.) compare all similar files (with the same hash)
2.) if the size is equal - remove file with longer path (calc by slashes!)
"""
