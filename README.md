# classio
A web app that aims to simplify course selection.

## Backend
### Data Structure for Database (Example used is CISC124)
ID: (doesn't matter just unique ID)
Name: CISC121
Constant Times: ...
Variable Times: ...

### Time Format
* **- seperates types** LEC...-LAB...-SEM...
* **: comes after a section type** LEC:...
* **; seperates sections of the same type** LEC:Mo12301330,We11301230,Th13301430;
* **, seperates times of the same section**

This format is used both in the raw read, and after section types are separated into variable and constant

LEC:Mo12301330,We11301230,Th13301430
Constant Times: LEC:Mo12301330,We11301230,Th13301430
Variable Times: LAB:We15301730,Mo18302030,Tu18302030,Fr15301730,Th1430-1630; ...

### Parse_class
Reads the classes from the stored format, fixes any repeats (since whoever organized the queen's db didnt!) andreturns a list of **course** objects. The main method is parse_request, all other methods are *'helpers'*.

### Optimizer
First, get the permutations of each class (CISC121: CV1W1, CV2W1, CV1W2, CV2W2)
Then, each permutation is looped through, checking for (and ignoring) conflicts, also testing for the earliest, latest and least time in between.
