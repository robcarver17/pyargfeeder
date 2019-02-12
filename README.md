# pyargfeeder

Easy command line access to python functions without maintaining scripts

Rob Carver

Version 0.0.2


20190212



## Description

This tiny tool is designed for easy command line access to frequently run python functions without having to maintain scripts or launch an interactive python session.

### Motivation

When running a large complicated trading system there are frequent times when the user needs to interact with the system, eg to get price data, change roll status, do manual trades,...


The two main methods for this are: 

- to launch a python prompt and then try and remember the command you want to run, plus where it is imported from
- to have various scripts


In my current system I use the scripts approach. I have a directory full of *command* (eg do a manual fill) scripts and a directory full of *diagnostic* scripts (eg get recent prices). 

Each interaction point then needs two files. Firstly a script like this (.profile just ensures we have the right PYTHONPATH):

```
#!/bin/bash
. ~/.profile
python $HOME/workspace/systematic_engine/syscontrol/mfill.py $1 $2 $3 $4
```

Then a *wrapper python* file like mfill.py:

```
import sys
from manualfill import manual_fill

if __name__=="__main__":

    if len(sys.argv)==2:
        if sys.argv[1]=="HELP":
            print "manualfill DBTYPE [LIVE, TEST, ...] IBtype [LIVE, TEST, ...] ORDERID [1,2,3,...] FILL [-2,-1,0,1,2]"
            print "Manually apply a fill to an order; mark an order as completed; unlock the positions table."
            sys.exit(0)

    print sys.argv
    
    if not len(sys.argv)==5:
        raise Exception("Need to supply exactly four arguments only type HELP")
    
    manual_fill(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
```

This calls the *underlying function* manual_fill.

Notice that the wrapper function does the following:

- provide help to the user
- check the right number of arguments has been supplied
- type cast certain arguments

Notice that it doesn't:

- know about defaults of the underlying function

Many of these functions will go on to ask for further information interactively. For example the above underlying function will also ask for the fill price when manual_fill is called.

This is all pretty fiddly, and with dozens of these scripts lying around they are a pain to maintain for example if the API of the underlying python functions changes.

### The solution

To replicate this kind of setup with `pyargfeeder` all you need to do is the following:

1- Copy the script file  [p](https://github.com/robcarver17/pyargfeeder/blob/master/pyargfeeder/p) to a script directory

2a- Change the run.py reference in the 'p' script file to point to the pyargfeeder module directory

OR

2b- Copy [run.py](https://github.com/robcarver17/pyargfeeder/blob/master/pyargfeeder/run.py) to a script directory (if you aren't worried about maintaining possible multiple copies of run.py)



3- At the command line type 

```
$ . p manualfill
```

Produces (with user typing shown inside asterix ):



```
Do a manual fill in the trading system

Manually apply a fill to an order; mark an order as completed; unlock the positions table.

Dummy function to test pyargfeeder package



Arguments:
['orderid', 'fill', 'fill_price', 'dbtype=LIVE', 'IBtype=LIVE']


Argument orderid   (type: int)?  *pressed return*
No default - need a value. Please type something!
Argument orderid   (type: int)?*45*
Argument fill   (type: int)?*yes*

Couldn't cast value yes to type int: retype or check commandlist.yaml

Argument fill   (type: int)?*-4*
Argument fill_price   (type: float)?*45.6*
Argument dbtype  (default: 'LIVE') ? *pressed return*
Argument IBtype  (default: 'LIVE') ?*TEST*

Done a fill of -4 for order 45 at price 45.600000 (LIVE, TEST)

Finished
```


Notice how:

- no command line arguments need to be given - everything has been done interactively
- some arguments have a default, entering an empty string by pressing return defaults to them
- some arguments have type casting (if annotations have been used in the argument signature). If something can't be cast, then you have to re-enter the value
- compulsory arguments (without defaults) have to have a value, you can't just press return

This is better, because:

- The 'help' information is always provided, and is produced by the doc string of the underlying function. So no extra documentation is required
- There is no need to remember and type long sequences of keyword arguments
- No need to launch a python interpreter
- No need to update a python wrapper function when the API of the underlying function changes.
- No need to update the script file to keep number of arguments in line


## Use and documentation


### Adding functions

Let's say you want to call a python function 'wibble' which is in the module fubar.thingy (can be anywhere that python can import from succesfully).  There are no restrictions on wibble, but it should have a doc string (ideally). It can have no arguments, or any number of named arguments with defaults, and positional arguments without defaults. Arguments can also have annotated types, or not.

```
def wibble(arg1, arg2: int, arg3="test", arg4=16.9):
    """
    This is a docstring
    """
    print(arg1)
    print(arg2)
    print(arg3)
    print(arg4)
```


Create a script directory.

1- Copy the script file  `p` to a script directory. This needs to be executable (in linux `chmod +x p`)
2a- Change the run.py reference in the 'p' script file to point to the pyargfeeder module directory

OR
2b- Copy [run.py](https://github.com/robcarver17/pyargfeeder/blob/master/pyargfeeder/run.py) to a script directory (if you aren't worried about maintaining possible multiple copies of run.py)



### Using the script


To call the script just type `$. p fubar.thingy.wibble`. The doc string for the function will be printed. You will then be prompted for each of the arguments of the underlying wibble() function. Example:

```
$. p fubar.thingy.wibble


This is a docstring  ## prints the docstring from wibble() function

Argument arg1  ? ## no default or type checking. You must type something, otherwise it will prompt again
Argument arg2    (type: int)? ## argument with type conversion. Any value you enter will be converted into the type shown. If this isn't possible it will prompt for the argument again
Argument arg3  (default: 'test') (type: str) ?   ## both defaults and type casting. Return will give you the default value. Otherwise value will be type converted.
Argument arg4  (default: '16.9')  (type: float)?   ## both defaults and type casting. Return will give you the default value. Otherwise value will be type converted.

```




### Documentation

There are two key files

- The 'p' script file
- The run.py


#### The 'p' script file

This does the setup of any dependencies and launches python on run.py with a single argument - the function reference (eg 'wibble'). It must be able to find run.py and be executable.

#### The run.py file

This imports the function, gets the arguments doing any type conversion.



## Dependencies

Python 3.3+


## Installation

This package isn't hosted on pip. So to get the code the easiest way is to use git:

```
git clone https://github.com/robcarver17/pyargfeeder.git
```



## Licensing and legal stuff

GNU v3

Absolutely no warranty is implied with this product. Use at your own risk. 

## Version history

v0.0.1 first release
v0.0.2 config file no longer required, uses type annotations
