"""
This code is highly inspired by 
https://gist.github.com/freeman-lab/330183fdb0ea7f4103deddc9fae18113
https://gist.github.com/freeman-lab/3e98ea4ccb96653c8fb085090079ce21

pip install thunder-python
pip install thunder-extraction
pip install thunder-registration
"""

import thunder as td
from extraction import NMF
from registration import CrossCorr
import numpy as np
import os
import json
import argparse

DEBUG = False

def main(args):
    datasets = ['00.00', '00.01', '01.00', '01.01', '02.00', '02.01', '03.00', '04.00', '04.01']
    base = '/Users/jerryhui/Downloads/project3_neurofinder.all.test/neurofinder.'
    submission = []

    for dataset in datasets:
        ds = dataset + '.test'
        path = os.path.join(base + ds, 'images')
        
        data = td.images.fromtif(path, stop=None, ext='tiff')
        if DEBUG:
            data = data[::10,:,:]
        print(data.shape)
        
        # median filter
        dataMF = registered.median_filter(size=2)

        # gaussian filter
        dataGF = dataMF.gaussian_filter(sigma=1)

        # registration
        algorithmReg = CrossCorr()
        modelReg = algorithmReg.fit(data, reference=data.mean().toarray())
        registered = modelReg.transform(data)

        algorithm = NMF(k=5, percentile=99, max_iter=50, overlap=0.1)
        model = algorithm.fit(dataGF, chunk_size=(50,50), padding=(25,25))
        merged = model.merge(0.1)
        
        regions = [{'coordinates': region.coordinates.tolist()} for region in merged.regions]
        result = {'dataset': ds, 'regions': regions}
        submission.append(result)
        print('%s has been finished' % ds)

    with open('submission.json', 'w') as f:
        f.write(json.dumps(submission))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Neuron Finding')
    args = parser.parse_args()
    main(args)
    