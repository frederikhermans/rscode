import ctypes
import os.path

import numpy as np
from numpy.ctypeslib import ndpointer

_rs = None


def _load():
    '''Load the RS implementation's shared library.'''
    global _rs

    if _rs is not None:
        return _rs

    path = os.path.join(os.path.dirname(__file__))
    sofiles = (path+'/reed_solomon-android.so', 'rscode.dll',
               path+'/reed_solomon.so')
    success = False
    for f in sofiles:
        try:
            _rs = ctypes.CDLL(f)
            success = True
        except OSError:
            # Failed to load this file, try next.
            pass
    if not success:
        raise RuntimeError('Couldn''t load shared rscode library. Please '
                           'see the rscode README.')

    _rs.init_rs.restype = ctypes.c_voidp
    _rs.init_rs.argtypes = (ctypes.c_int,  # symsize
                            ctypes.c_int,  # gfpoly
                            ctypes.c_int,  # fcr
                            ctypes.c_int,  # prim
                            ctypes.c_int)  # nroots

    _rs.encode_rs8.restype = ctypes.c_int
    flags = 'C_CONTIGUOUS'
    _rs.encode_rs8.argtypes = (ctypes.c_voidp,   # rscontrol
                               # uint8_t *data
                               ndpointer(ctypes.c_uint8, flags=flags),
                               ctypes.c_int,     # len
                               # uint16_t *par
                               ndpointer(ctypes.c_uint16, flags=flags),
                               ctypes.c_uint16)  # invmask

    _rs.decode_rs8.restype = ctypes.c_int
    _rs.decode_rs8.argtypes = (ctypes.c_voidp,   # rscontrol
                               # uint8_t *data
                               ndpointer(ctypes.c_uint8, flags=flags),
                               # uint16_t *par
                               ndpointer(ctypes.c_uint16, flags=flags),
                               ctypes.c_int,     # len
                               ctypes.c_voidp,   # uint16_t *s
                               ctypes.c_int,     # no_eras
                               ctypes.c_voidp,   # eras_pos
                               ctypes.c_uint16,  # invmask
                               ctypes.c_voidp)   # corr

    _rs.free_rs.restype = None  # void
    _rs.free_rs.argtypes = (ctypes.c_voidp, )

    return _rs


class RSCode(object):
    def __init__(self, parity_len):
        self.parity_len = parity_len
        if self.parity_len == 0:
            return
        self.rs = _load()
        self.rs_struct = self.rs.init_rs(8, 0x187, 0, 1, parity_len)

    def encode(self, data):
        '''Encode the uint8 array `data`.

        A new array which contains the input data concatenated with the
        parity.'''
        if data.dtype != np.uint8 or len(data) >= 255:
            raise ValueError('Invalid data format.')

        if self.parity_len == 0:
            return data
        par = np.zeros(self.parity_len, dtype=np.uint16)
        self.rs.encode_rs8(self.rs_struct, data, len(data), par, 0)
        assert np.all(par < 256)
        data_with_par = np.concatenate((data, par.astype(np.uint8)))
        return data_with_par

    def decode(self, data_with_par):
        '''Decodes an uint8 array containing data followed by parity.

        Returns the number of corrected errors and the reconstructed data. If
        recovery is known to have failed, a negative number is returned along
        with the input data.

        Note that `data_with_par` is updated, as the decoding is performed
        in-place.'''
        if not data_with_par.dtype == np.uint8:
            raise ValueError('Invalid data format.')
        if self.parity_len == 0:
            return 0, data_with_par
        n = len(data_with_par) - self.parity_len
        par = data_with_par[-self.parity_len:].astype(np.uint16)
        retval = self.rs.decode_rs8(self.rs_struct, data_with_par, par, n,
                                    None, 0, None, 0, None)
        return retval, data_with_par[:-self.parity_len]

    def free(self):
        '''Frees internal resources associated with the code.'''
        if self.parity_len == 0:
            return
        self.rs.free_rs(self.rs_struct)
        self.rs = None
        self.rs_struct = None
