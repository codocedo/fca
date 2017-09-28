# uncompyle6 version 2.12.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.13 |Continuum Analytics, Inc.| (default, Dec 20 2016, 23:05:08) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/victorcodocedo/Work/kyori_lab/github/fca/examples/ex10_dg_imp_base_nc.py
# Compiled at: 2017-09-27 11:45:18
from __future__ import print_function
import argparse
from fca.reader import FormalContextManager
from fca.algorithms.canonical_base import CanonicalBaseNC

def exec_ex10(filepath, min_sup=0):
    """
    Example 10 - Obtains the Duquenne-Guigues Canonical Base
    of Implications Rules with NextClosure
    """
    canonical_base = CanonicalBaseNC(FormalContextManager(filepath=filepath), min_sup=min_sup, lazy=False)
    for rule, support in canonical_base.get_implications():
        ant, con = rule
        print('{}=>{}'.format(ant, con), support)


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 10 - Obtains the Duquenne-Guigues Canonical Base\n                       of Implications Rules with NextClosure\n                    ')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context in txt, space separated values, one object representation per line')
    __parser__.add_argument('-m', '--min_sup', metavar='min_sup', type=float, help='Relative minimum support [0,1]', default=0.0)
    __args__ = __parser__.parse_args()
    exec_ex10(__args__.context_path, __args__.min_sup)
# okay decompiling ex10_dg_imp_base_nc.pyc
