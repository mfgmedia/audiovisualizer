import os
import json
from pprint import pprint

from collections import defaultdict as ddict

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

sample_dir = '/Volumes/Personals/marcel.gellesch/Downloads/musicradar-hiphop-samples/resample'


def get_path(path_name):
    return os.path.join(ROOT_DIR, path_name)


def get_relative_path(path_name):
    return path_name.split(sample_dir)[-1].lstrip('/')


def get_subdirectories(dir):
    path = get_path(dir)
    for dirpath, dirname, filenames in os.walk(path):
        # print(dirpath, dirname, filenames)
        if dirpath == path:
            return dirname


def get_files(dir):
    path = get_path(dir)
    print(path)
    for dirpath, dirname, filenames in os.walk(path):
        print(dirpath, dirname, filenames)
        if dirpath == path:
            return tuple((fname, f'{get_relative_path(dirpath)}/{fname}') for fname in filenames)


def get_bundles():
    return get_subdirectories(sample_dir)


def get_instruments(bundle):
    return get_subdirectories(f'{sample_dir}/{bundle}')


def cluster_files(files):
    result = {}
    for f, full in files:
        x, y = f.split(' ')
        result.setdefault(x, {})[y.split('.')[0]] = full
    return result


def get_tracks(bundle, instrument):
    files = get_files(f'{sample_dir}/{bundle}/{instrument}')

    return cluster_files(files)


if __name__ == '__main__':
    result = {bundle:
                  {'tracks':
                       {inst: get_tracks(bundle, inst) for inst in get_instruments(bundle)}
                   }
              for bundle in get_bundles()}

    for k, v in result.items():
        with open(f'{sample_dir}/{k}.json', 'w') as fp:
            json.dump(v, fp)

