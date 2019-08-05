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

**new addition: section types separated by ';' now contain the section number first numb?... The number ends with a question mark**

LEC:Mo12301330,We11301230,Th13301430
Constant Times: LEC:Mo12301330,We11301230,Th13301430
Variable Times: LAB:2112?We15301730,Mo18302030;1212?We11301230,Mo17301830 ...

### Parse_class
Reads the classes from the stored format, fixes any repeats (since whoever organized the queen's db didnt!) andreturns a list of **course** objects. The main method is parse_request, all other methods are *'helpers'*.

#### Ledger for class nums (Each class has one!)
[ ['LEC', [ [{[1times.....], [nums1]}], [{[2times......], [nums2]}] ]], ...]

### Optimizer
First, get the permutations of each class (CISC121: CV1W1, CV2W1, CV1W2, CV2W2)
Then, each permutation is looped through, checking for (and ignoring) conflicts, also testing for the earliest, latest and least time in between.

## Scrapers
Real quick list of university rankings
 Waterloo - S
 UBC - B
 Queen's - D (passed but nothing to be proud of)

* Waterloo has a solid api, which is down! Data is scraped with requests and BeautifulSoup.
* UBC is yet to be seen, but it looks like they might need me to use selenium, though much less then Queen's from not needing to log in!
* Queen's right now works by me logging in, letting selenium loose, and waiting for an hour or two to scrape all the data. Not only is it user-intensive, it requires my half-attention for any debugging. The process of searching for a class is very slow, so the database is usually old. However, it seems like Queen's doesnt update course info often anyway.
