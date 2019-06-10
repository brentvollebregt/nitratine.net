title: "Remove Columns in a CSV File With Python"
date: 2019-06-10
category: Tools
tags: [python, csv]
feature: feature.png
description: "Need to remove columns from a large CSV file? Simply provide this script the indexes of columns you want to be deleted and it will create a copy CSV file with those columns removed."

[TOC]

## What is This?
This script takes an input CSV file and outputs a copy of the CSV file with particular columns removed. Provide `cols_to_remove` a list containing the indexes of **columns** in the CSV file that you want removed (starting from index 0 - so the first column would be 0).

I have used indexes because they are easier to use programmatically and if I did use header titles, one character or space would have put it off. This method scales very well and can remove columns where MS Execl can't open a large file.

## Code

```python
import csv

input_file = 'input.csv'
output_file = 'output.csv'
cols_to_remove = [1, 4, 10, 11] # Column indexes to be removed (starts at 0)

cols_to_remove = sorted(cols_to_remove, reverse=True) # Reverse so we remove from the end first
row_count = 0 # Current amount of rows processed

with open(input_file, "r") as source:
    reader = csv.reader(source)
    with open(output_file, "w", newline='') as result:
        writer = csv.writer(result)
        for row in reader:
            row_count += 1
            print('\r{0}'.format(row_count), end='') # Print rows processed
            for col_index in cols_to_remove:
                del row[col_index]
            writer.writerow(row)
```