# classio
A webapp that aims to simplify course selection.

## Data Structure for Course (Example used is CISC124)
  ID: (doesn't matter just unique ID)
  Name: CISC121
  ###TIME FORMAT
  * **- seperates types** LEC...-LAB...-SEM...
  * **: comes after a section type** LEC:...
  * **; seperates sections of the same type** LEC:Mo12301330,We11301230,Th13301430;
  * **, seperates times of the same section**

  This format is used both in the raw read, and after section types are separated into variable and constant


  LEC:Mo12301330,We11301230,Th13301430
  Constant Times: LEC:Mo12301330,We11301230,Th13301430
  Variable Times: LAB:We15301730,Mo18302030,Tu18302030,Fr15301730,Th1430-1630; ...

## How permutations are checked for conflicts
  Obviously any timetable that has conflicts should not be displayed. Firstly, the constant times are checked for conflicts
