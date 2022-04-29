from fca.algorithms import dict_printer
from fca.io import read_representations
import json

import argparse
parser = argparse.ArgumentParser(description='FCA for Python')
parser.add_argument('-i', '--input_context', metavar='context_path', type=str, help='path to the input formal context')
parser.add_argument(
    '-a',
    '--algorithm',
    choices=['a', 'c', 'n'],
    metavar='algorithm',
    type=str,
    help='[a]ddIntent, [c]bo, [n]ext_closure'
    )

parser.add_argument('-o', '--output', action='count', help='Output options: -o number of concepts; -oo list of concepts; -ooo json output', default=1)
parser.add_argument('-m', '--abs_min_sup', metavar='min_sup', type=int, help='Absolute Minimum Support [0, inf]', default=0)
parser.add_argument('-s', '--min_sup', metavar='min_sup', type=float, help='Relative Minimum Support [0, 1]', default=0.0)
parser.add_argument('--lazy', help='Compute closure lazily', action='store_true')
# parser.add_argument('-t', '--theta', metavar='theta', type=int, help='Maximal length for intervals [0,inf]', default=0)

args = parser.parse_args()

if args.algorithm == 'a':
    from fca.algorithms.addIntent import AddIntent
    assert bool(args.min_sup) is False, "ERROR: AddIntent doesn't admit relative minimum support\nFIX: Instead, provide an absolute value for the support with -m"
    if args.abs_min_sup:
        from fca.defs.patterns import IcebergSetPattern
        IcebergSetPattern.reset() 
        IcebergSetPattern.MIN_SUP = args.abs_min_sup
        poset = AddIntent(
                read_representations(args.input_context, transposed=True),
                pattern=IcebergSetPattern,
                lazy=args.lazy,
                silent=False
            ).lat
        if (args.output <= 2):
            print("Number of Concepts:", len(poset.concept))
        elif(args.output == 3):
            dict_printer(
                poset,
                transposed=True,
                indices=False
            )
        else:
            print(json.dumps(poset.concepts()))
    else:
        poset = AddIntent(
                read_representations(
                    args.input_context),
                lazy=args.lazy
            ).lat
        if (args.output <= 2):
            print("Number of Concepts:", len(poset.concept))
        elif(args.output == 3):
            dict_printer(
                poset
            )
        else:
            print(json.dumps(poset.concepts()))

elif args.algorithm == 'n':
    from fca.algorithms.lecenum_closures import LecEnumClosures
    from fca.io.input_models import FormalContextModel
    assert bool(args.abs_min_sup) is False, "ERROR: NextClosure doesn't admit absolute minimum support\nFIX: Instead, provide a relative value for the support with -s"
    poset = LecEnumClosures(
            FormalContextModel(
                filepath=args.input_context),
                min_sup=args.min_sup,
                lazy=args.lazy,
                silent=False
        ).poset
    if (args.output <= 2):
        print("Number of Concepts:", len(poset.concept))
    elif(args.output == 3):
        dict_printer(
            poset
        )
    else:
        print(json.dumps(poset.concepts()))
elif args.algorithm == 'c':
    from fca.algorithms.cbo import CbO
    from fca.io.input_models import FormalContextModel
    assert bool(args.abs_min_sup) is False, "ERROR: CbO doesn't admit absolute minimum support\nFIX: Instead, provide a relative value for the support with -s"
    poset = CbO(
            FormalContextModel(
                filepath=args.input_context),
            min_sup=args.min_sup,
            lazy=args.lazy,
            silent=False
        ).poset
    if (args.output <= 2):
        print("Number of Concepts:", len(poset.concept))
    elif(args.output == 3):
        dict_printer(
            poset
        )
    else:
        print(json.dumps(poset.concepts()))