import unittest

import numpy as np
from .rscode import RSCode


class Test(unittest.TestCase):
    def test_code_decode(self):
        parity_len = 32
        ntests = 1000

        code = RSCode(parity_len)
        data = np.random.randint(0, 255, 64).astype(np.uint8)
        n = len(data)
        data_with_par = code.encode(data)
        for nerrors in xrange(0, parity_len/2+1):
            for _ in xrange(ntests):
                data_err = data_with_par.copy()
                # Introduce `nerrors` errors
                for pos in np.random.choice(range(n), nerrors, replace=False):
                    data_err[pos] ^= np.random.randint(1, 255)
                retval, repaired = code.decode(data_err)
                self.assertTrue(np.all(data == repaired))
                self.assertEqual(retval, nerrors)
        code.free()
