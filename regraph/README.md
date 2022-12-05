About
=====

Regraph is a python program used to genereate number or timestamp line
graphs from standard input. The data is extracted based on a regular 
expression.


How it works
============

The data is extracted based on a regular expression, that can be customized
through the command line (-r option), or rely on its default value.

The type of plots can be number against number or timestamp against number.
The timestamp format is very flexible, ranging from simple HH:MM:SS format
to the more complex YYYY-mm-dd HH:MM:SS.milisecond. In fact, the program
will try guess what is the timestamp in a very flexible way, so don't worry
about the details. Probably, any date that you can understand the program
will also understand, including strings like 'Jan 1' or 'Jan 1 2010'.

The axis labels must be provided on the first line of text, and the program
will extract it with the same regular expression to fetch the data. 
It is considered as a label if the fields in the first line are not numbers nor
timestamps. If you omit the axis labels there is no problem, the program
will simple call them x and y.

The program can be verbose or not (-v option). In the verbose version
every action is printed to standard output, telling what is being done
for each line of text.

The generated graph will be saved in the user's home or desktop directory.
If the path '~/Desktop' or '~/desktop' exists, the file will be saved there, 
otherwise in '~'. This directory can be choosed from the -d option.
The output file name will be 'x_axis-y_axis-YYYYmmddHHMMSS.png'. You can
also customize the file type from -t option, that can be: png, jpg, pdf, eps,
ps or csv.


Install
=======

From the source directory, as root, you need to run:

!# python setup.py install


Dependencies
============

- Python >= 2.5
- Matplotlib


Author
======

Guilherme Starvaggi Franca

Feel free to send messages about bugs.


