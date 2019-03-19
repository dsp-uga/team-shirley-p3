"""
This code is highly inspired by 
https://gist.github.com/freeman-lab/330183fdb0ea7f4103deddc9fae18113
https://gist.github.com/freeman-lab/3e98ea4ccb96653c8fb085090079ce21

"""

import thunder as td
from extraction import NMF
import numpy as np
import os
import json
import argparse

DEBUG = True

def main(args):
    datasets = ['00.00', '00.01', '01.00', '01.01', '02.00', '02.01', '03.00', '04.00', '04.01']
    base = '/Users/jerryhui/Downloads/project3_neurofinder.all.test/neurofinder.'
    submission = []

    for dataset in datasets:
        ds = dataset + '.test'
        path = os.path.join(base + ds, 'images')
        if DEBUG:
            data = td.images.fromtif(path, stop=50, ext='tiff')
        else:
            data = td.images.fromtif(path, stop=None, ext='tiff')
        
        data.gaussian_filter()

        algorithm = NMF(k=5, percentile=99, max_iter=50, overlap=0.1)
        model = algorithm.fit(data, chunk_size=(50,50), padding=(25,25))
        merged = model.merge(0.1)
        
        regions = [{'coordinates': region.coordinates.tolist()} for region in merged.regions]
        result = {'dataset': ds, 'regions': regions}
        submission.append(result)
        print('%s has been finished' % ds)

    with open('submission.json', 'w') as f:
        f.write(json.dumps(submission))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Neuron Finding')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-tr', '--train', action='store_true', help='Whether or not to train (hyper-parameter tuning)')

    args = parser.parse_args()
    main(args)