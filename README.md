Deck Building Card Game 
-------------------------------
[![Build Status](https://travis-ci.com/nikos912000/sd-card-game.svg?token=zU6ptnBBwDGu1jzbrQNz&branch=master)](https://travis-ci.com/nikos912000/sd-card-game)

Final version of the Deck Building Card game. 

This assignment has been completed under the "Software Development" course at the University of Edinburgh.

## LICENSE
Copyright (c) 2016 Nikos Katirtzis - All rights reserved

## Dependencies
There are no dependencies on third-party libraries in order to run the program. However, you will need the `nose`, `coverage` and `mock` libraries to run our test suite, as well as the `pylint` library to check the score achieved. Although these libraries should be installed in the cplab computers, you can use the `requirements.txt` file to install them in case they are not. You can install the libraries from the `requirements.txt` using:

`pip install requirements.txt`

If the `pip` command is not available, you can install it in the user's account using:

`easy_install --user pip`

After that, you can install the `requirements.txt` using:

`/home/XXX/.local/bin/pip install --user -r requirements.txt`

where XXX is your username.

This will install the `nosetests` library in the user's account. Thus, you need to modify the `nosetests.sh` script as follows:

`/home/XXX/.local/bin/nosetests --with-coverage --cover-package=deckgame`

where XXX is again your username.

You may need to proceed to the same modification to the `pylint.sh`script, too.

In case you still have a problem running the test suite, you can check the results of our test suite by clicking on the Travis icon ("build passing") provided at the top of this file!


## How to run the application
You can run the application using the following command:

`python main.py`

## How to execute the tests
Considering that you have installed the required libraries, you can run our test suite using:

`sh nosetests.sh`

## How to run Pylint for our project
Considering that you have installed the required libraries, you can run pylint using:

`sh pylint.sh`

## How to run pydoc for our project
The code is documented with Python docstrings. An interactive documentation browser is available by running:

`pydoc -p <PORT>`
