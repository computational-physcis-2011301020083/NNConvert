#!/usr/bin/env python3

"""
Build an input specification file for Wei's NN
"""

from h5py import File
from argparse import ArgumentParser
import numpy as np
import json
import sys

def get_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mean_std_file')
    return parser.parse_args()

def mkvar(name, shift, scale):
    return dict(name=name, offset=shift, scale=scale, default=-shift)

def mknode(name, variables):
    return {
        'name': name,
        'variables': [mkvar(*v) for v in variables]
    }

def run():
    args = get_args()
    with File(args.mean_std_file,'r') as h5file:
        mean = np.asarray(h5file['mean'])
        std = np.asarray(h5file['std'])

    out_dict = {
        "input_sequences": [],
        "outputs": [
            {
                "labels": ["QCD", "Higgs", "Top"],
                "name": "Xbb2020v2"
            }
        ]
    }
    scale_arr = 1 / std.flatten()
    shift_arr = -mean.flatten()
    valiter = zip(shift_arr, scale_arr)
    fatshift, fatscale = (x / 1000 for x in next(valiter))
    etavars = next(valiter)
    inputs = [
        mknode('fatjet', [
            ('pt', fatshift, fatscale), ('eta', *etavars)]
        )
    ]
    dl1_names = [f'DL1r_p{x}' for x in 'ucb']
    for n in range(3):
        dl1s = [(nm, *v) for nm, v in zip(dl1_names, valiter)]
        inputs.append(mknode(f'subjet{n}', dl1s))

    out_dict['inputs'] = inputs

    sys.stdout.write(json.dumps(out_dict, indent=2))

if __name__ == '__main__':
    run()
