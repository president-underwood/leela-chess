#!/usr/bin/env python3
import tensorflow as tf
import os
import sys
import yaml
from tfprocess import TFProcess

cfg = yaml.safe_load(open(sys.argv[1], 'r').read())
print(yaml.dump(cfg, default_flow_style=False))

with open(sys.argv[2], 'r') as f:
    weights = []
    for e, line in enumerate(f):
        if e == 0:
            #Version
            print("Version", line.strip())
            if line != '1\n':
                raise ValueError("Unknown version {}".format(line.strip()))
        else:
            weights.append(list(map(float, line.split(' '))))
        if e == 2:
            channels = len(line.split(' '))
            print("Channels", channels)
    blocks = e - (4 + 14)
    if blocks % 8 != 0:
        raise ValueError("Inconsistent number of weights in the file")
    blocks //= 8
    print("Blocks", blocks)

tfprocess = TFProcess(cfg)
tfprocess.init(1)
if tfprocess.RESIDUAL_BLOCKS != blocks:
    raise ValueError("Number of blocks in tensorflow model doesn't match "\
            "number of blocks in input network")
if tfprocess.RESIDUAL_FILTERS != channels:
    raise ValueError("Number of filters in tensorflow model doesn't match "\
            "number of filters in input network")
tfprocess.replace_weights(weights)
path = os.path.join(os.getcwd(), cfg['name'])
save_path = tfprocess.saver.save(tfprocess.session, path, global_step=0)
