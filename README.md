# Gambet 🤔

Gambet is a numbers guessing game of wit and strategy.
The object of the game is for you to outwit and beat Gambet.
You guess Gambet’s number, and Gambet guesses your number.
Both yours and Gambet’s numbers must consist of four different digits from 1 to 9.

## How to play


In the onscreen playing section, you must select and enter a four digit number that you believe matches Gambet’s number.
After entering this number the program will give you two values, and these will appear in the player list.
Then Gambet will show you a number that it thinks matches your number, and two values "B" and "S" that will show on screen.

The *B* value indicates the amount of numbers that you have selected and match Gambet’s numbers, but in different places.

The *S* value indicates the amount of numbers that you have selected and match Gambet’s numbers that are in the correct place.

## Getting Started

These project is written in python using **Kivy** library for graphical interface, to run this project we need only to install **kivy** library.
### Prerequisites

To install kivy in windows, you can follow this instructions : 

```
python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.gstreamer --extra-index-url https://kivy.org/downloads/packages/simple/
python -m pip install kivy
```

## Running Gambet

To run this game, you have only to run the **main.py** file, then choose whether to play against the program ( with Gambet ) or just try to guess his number ( single ). 

### The Algorithm

The algorithm used in that game to guess your number is producing all the possibilities that matches the *B* and *S* values given for the number tested by Gambet.

```
number : 1234 B : 4 S : 0
possibilities : {'4132', '2134', '3241', '1423', '4321', '4231', '1234', '2413', '3142', '3214', '1243', '1342', '1324', '4213', '4312', '1432', '2431', '3124', '3412', '2314', '4123', '3421', '2341', '2143'}
```

## Notes
This project is written on Februray 2017, as an android app that has been published on google play [Gambet](https://play.google.com/store/apps/details?id=mais.gambet&hl=en), and has been updated on January 2018.
I have used python-to-android project that uses buildozer to generate an apk file from python code.

## Built With 🏗️

* [Python3](https://www.python.org/) - python
* [Kivy](https://kivy.org/) - The graphical interface library
* [buildozer](https://kivy.org/doc/stable/guide/packaging-android.html) - Used to generate an android excutable file (apk).

## Authors ✍

* **Said Mohamad Ammar** - *Student in Lille University* 
