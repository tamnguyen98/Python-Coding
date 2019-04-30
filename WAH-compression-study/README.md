# WAH compression study

# About
This is assignment Four for WSU-V CS 351. The purpose of this program is to learn about VAL compression. The task is
> Read a given data table (Data/animals.txt, Data/anaimals_test.txt, and Data/anaimals_test_sorted.txt), convert it to
bitmap, and compress it with 32/64 bit VAL compression. The *_bitmap* and *_compressed* are given to compare accuracy
my compression to the professor's. Additionally, it's required that students needs to not only convert and compress the
original file but also do the same for a sorted version of the data file (the program will automatically sort (unless specified
with -nosort) and give both version of the data file (sort/original)).

Requirement:
Python 3.X installed on your system to run (could possibly work with lower version).

The following files were provide prior to starting the assignment:
- Whole Data folder

### Features

- Nothing special really...

### How to use
Run the following commands
```
> py Main.py <-nosort (optional)> <data file> <(Optional) 32/64 bit compression>

```
The program will spit out both the bitmap and compressed result in the same directory as the data file. It will be named 
```
x_bitmap.txt
x_bitmap_compressed_32.txt
x_bitmap_compressed_64.txt
x_bitmap_sorted.txt
x_bitmap_sorted_compress_32.txt
x_bitmap_sorted_compress_64.txt
```
where x is the file name and directory (excluding the extention) and y being the compression bits value.
#### Example
```
> py Main.py Data/animals_test.txt 32 # For 32 bit word compression of both sorted and unsorted bitmaps.
> py Main.py Data/animals_test.txt # For both 32 and 64 bit.
> py Main.py -nosort Data/animals_test.txt # For both 32 and 64 bit compression of original data only.
```