## Antlife - TPT09

### Requirements

- Python3
- PyQt4
- Evolife [http://evolife.dessalles.fr/](http://evolife.dessalles.fr/)

The program has the same requirements as Evolife, namely a python interpreter and PyQt4. The program has been tested using Python 3.5.1.

### Structure

The structure contains four folders

| folder | description |
| ------ | ----------- |
| bin/ | Contains a script to execute the finished program, as well as a helper script to properly “install” Evolife. |
| libs/ | Contains libraries, for now just a Evolife version. |
| res/ | Contains resources used, namely .xml config files, images, .evo parameter files, and results get moved here when the program finishes execution. |
| src/ | Contains the Python source code. |

### Running the program
1. Download Antlife.zip and unzip it.
2. ```cd libs/ && unlink Evolife.zip``` # Then either drop in your copy of Evolife.zip or use eg. ```ln -s Evolife-2016-03-17.zip
Evolife.zip``` to just link to a specific download of the Evolife package.
3. ```./bin/evolifer``` # to unzip Evolife, and run first.py
4. ```PYTHONPATH=$PYTHONPATH:libs/ ./bin/antlife``` # to run the modified Ants program 

Alternatively add export PYTHONPATH=“${PYTHONPATH}:libs/“ below line 5 in the file bin/
antlife to fix the bug in the submitted code, and be able to just run ```./bin/antlife```

This runs ants.py, a modified version of Other/Ants/Ants.py with all the classes extracted to
their own files.
