# Instructions

At Holaluz we are worried about fraud in electricity readings and we have decided to implement a suspicious reading detector.

Some clients have phoned us suspecting some squatters have been tapping into their electricity lines and this is why you may find some extremely high readings compared to their regular usage.
At the same time, we suspect some clients are tapping their building electricity lines and you may also find extremely low readings.

As we all know, many systems in Spain are a bit old fashioned and get some readings in XML and some others in CSV, so we need to be able to implement adaptors for both inputs.

For this first iteration, we will try to identify readings that are either higher or lower than the annual median ± 50%.

Please write a command line application that takes a file name as an argument (such as 2016-readings.xml or 2016-readings.csv) and outputs a table with the suspicious readings:
```
| Client              | Month              | Suspicious         | Median
 -------------------------------------------------------------------------------
| <clientid>          | <month>            | <reading>          | <median>
````

You can assume there are no tricks in the XML and CSV files. Each client will have 12 readings and you get all 12 consecutively. Please don't spend time trying to validate all this although it happens in real life sometimes!

In this exercise, we are looking for things like:

   - An explanation on how to run the tests and the code, how to install the requirements, etc.
   - Hexagonal architecture to handle different inputs (CSV and XML in this case, but it could be a database or even a txt file in a remote FTP! True story...)

 Bonus points if you use:
   - Idiomatic features of the language
   - Automated tests

The solution can be written in any of our stack languages: PHP, Python or Java, and will be great if we can see the development process with a .git folder.

You can use any external library or language version, but please, make us as easy as possible to reproduce your development environment conditions, in the way you consider.


# ReadingDetector

Exercise for HolaLuz for a fraud reading detector


# Installation

It is typical to use some type of virtualenv (venv, conda, etc...) to install code and execute. One option can be venv and something like this:

    $ python3 -m venv exercise-env
    $ source exercise-env/bin/activate
    $ pip install -r requirements
    $ pip install -e .

# Usage

To use it:

    $ reading-detector name_file.csv

# TEST

    $ pytest

In my case, I use makefile and I trigger this script every time with something like this: makefile -f Makefile.vim

# Architecture design

It is implemented a  hexagonal architectures  with ports (app.py), adapters (adapters.py) and an application (app.py) with its business logic.

- It was discarded the application of services and use cases classes in the design because the problem is too small, to avoid an overdesign
- It was discarded to use in memory or DB repositories to avoid overdesign. For this, this app-cli is syncron., It means we wait for a result and we are not running
processes or threads.

- I added two fraud detectors a personal implemetation and the demanded for the exercise:
	- The first one version  has hardcoded threshold and the global threshold doesn t apply any normalization, it means one necessary improvement can be normalized (it was not done for time)
	- AN IMPORTANT POINT. I Added global threshold in the ML adapter that it filter only the most big frauds. It can be removed to provide more sensitive solutions, but how we are using a small dataset I prefered to keep it.
- It is applied acceptance tests (end-to-end) and functional tests for each module, if the code starts to be bigger it can be applied the pyramid test.
- One pending point to finish is the logging. I added one logger in the cli but if the code starts to be too much complicate it can be added in more places.
