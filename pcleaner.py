import os
import json
import hashlib


TARGED_DIRECTORY = "/Users/cold00n/SAMPLES/_projects/"
FILENAME = "./pcleaner_outfule.json"


def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def getsubs(path):
    # get all

    paths = []
    index = {}
    diff = {}

    def update_index(file_path, file_hash, size):
        """
        Update dictionary 'index' by:
        KEY: :param file_hash:
        and
        VALUE: [:param size:, :param file_path:]
        """
        if file_hash in index:
            # Update value for existent key
            index[file_hash].append([size, file_path])
            diff.update({file_hash: index[file_hash]})
        else:
            # Add new key
            index.update({file_hash: [[size, file_path]]})

    for path_name, path_names, file_names in os.walk(path):

        paths.append(path_name)

        for sub_path_name in path_names:
            paths.append(os.path.join(path_name, sub_path_name))

        for file_name in file_names:
            full_path = os.path.join(path_name, file_name)
            try:
                size = os.path.getsize(full_path)
            except OSError:
                pass
            else:
                update_index(full_path, hashfile(full_path), size)

    return diff


data = getsubs(TARGED_DIRECTORY)
with open(FILENAME, 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False)

"""
with open(FILENAME) as infile:
    data = json.load(infile)
"""




"""
1.)calc size profit after removing!!!

implement removing algorithm:
1.) compare all similar files (with the same hash)
2.) if the size is equal - remove file with longer path (calc by slashes!)
"""
