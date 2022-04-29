# fca - Python Libs for FCA

## License
GPL V3

## Requirements
The library has no dependencies and is entirely written over standard Python libs.
As a result, fca can be executed over python and pypy.

## Install

This library is available from PyPi:
```pip install fca```

## Examples
The folder ```examples``` contain some scripts showing the capabilities of the library.

To execute all examples:

```python all_examples.py```

## Tests
Some Unitary tests are provided for this library in directory ```tests```.

To execute tests for the input model:
```python test_InputModel.py```

## 5.- Formats
Currently, the library supports comma separated values (```CSV```), space separated values (```SSV```) and ```CXT``` files.

Formats are inferred from extensions with extension ```.txt``` defaulting to ```SSV``` format.

Both, ```CSV``` and ```SSV``` consider one line per object. Attributes are read as strings.

## Algorithms
Three main algorithms for FCA are currently supported:
- AddIntent: Calculates a Concept Lattice incrementally. By design, AddIntent does not consider a minimum support thresholding, however a mechanism based on projections has been implemented so an Iceberg Lattice can technically be built by transposing the formal context and then, the roles of extents and intents. However, it will always have bottom concept, regardless of its support. AddIntent only takes an absolute minimum support value.
- NextClosure: Calculates a set of formal concepts using the next closure algorithm. It takes a relative minimum support value.
- Close-by-One (CbO): Calculates a set of formal concepts using the close-by-one algorithm. It takes a relative minimum support value.

## Output
There are three levels of default:
- [-o] (default value) : Prints the number of formal concepts calculated
- [-oo]: Prints a list of formal concepts
- [-ooo]: Outputs the list of formal concepts in json format. At this point, the json format considers an internal representation of formal concepts and not the actual representation. This is, attributes will be represented by numbers with no relation to the actual label of an attribute. This should be fixed in a future version.