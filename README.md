# Reed-Solomon coding in Python #

This is a simple Python wrapper around a RS implementation that was yanked
from the Linux kernel (https://github.com/tierney/reed-solomon).

Wrapper written by Frederik Hermans (frederik.hermans@it.uu.se), with
modifications for Win32 by Gábor Sörös (https://people.inf.ethz.ch/soeroesg/).

## Install ##

You need to build the shared library for this Python module to work.
Simply run `make` in the `c-src` directory.

## Example ##

    import rscode
    import numpy as np

    # Our data is going to be 16 random bytes
    data = np.random.randint(0, 255, 16).astype(np.uint8)

    code = rscode.RSCode(4) # Code that can correct up to two errors
    encoded = code.encode(data)

    # Make some changes
    encoded[0] = 42
    encoded[17] = 23

    # Decode and print results
    ncorrected, decoded = code.decode(encoded)
    print 'Corrected errors:', ncorrected
    print 'Decoded data matches original data:', np.all(decoded == data)


## Testing ##

Run `nosetests` in the `rscode` directory.
