# py4madx
Python scripts to use with cpymad.

Some of the scripts are translations to py of existing ones in madx, available in the LHC optics direcotry: **/afs/cern.ch/eng/lhc/optics/**

## Instructions how to use and isntall the package:

### Installation

Use the command from your terminal : 

```
pip install --user git+https://github.com/iefthymio/py4madx.git
```

or for upgrades:

```
pip install --upgrade --user git+https://github.com/iefthymio/py4madx.git
```

### Usage

```
import py4madx
from py4madx import pmadx
from py4madx import beambeam
from py4madx import qslice

py4madx.my_cool_test_method()
It works!

pmadx.Version
```

## Acknowledgments

Instructions how to setup this project were found in : https://dev.to/rf_schubert/how-to-create-a-pip-package-and-host-on-private-github-repo-58pa


