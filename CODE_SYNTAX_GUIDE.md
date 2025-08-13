# Line-by-Line Code Syntax Guide 🔍

*Every line explained in simple terms*

---

## Lines 1-30: File Header & Imports

```python
#!/usr/bin/env python3
```
**Syntax:** `#!` = shebang, tells computer this is a Python 3 script
**Plain English:** "This is a Python 3 program"

```python
"""
NASA Models Team CR Support Report - Simple Version
"""
```
**Syntax:** `"""` = multi-line string (docstring)
**Plain English:** "This text describes what the program does"

```python
import os
import csv
import sys
import re
```
**Syntax:** `import modulename` = bring in external tools
**Plain English:** 
- `os` = file and folder operations
- `csv` = spreadsheet file handling  
- `sys` = system stuff (command line arguments)
- `re` = text pattern matching (regex)

---

## Lines 31-45: Main Function Start

```python
def main():
```
**Syntax:** `def functionname():` = create a function
**Plain English:** "Start the main program function"

```python
if len(sys.argv) < 2:
```
**Syntax:** `if condition:` = check if something is true
- `len()` = count items in a list
- `sys.argv` = list of command line arguments
- `< 2` = less than 2
**Plain English:** "If user didn't give us a folder path"

```python
print("Error: Please provide folder path")
```
**Syntax:** `print("text")` = show text on screen
**Plain English:** "Show this error message"

```python
sys.exit(1)
```
**Syntax:** `sys.exit(number)` = stop the program
- `1` = error code (0 = success, 1+ = error)
**Plain English:** "Stop the program with error"

```python
folder_path = sys.argv[1]
```
**Syntax:** `variable = value` = store something in memory
- `sys.argv[1]` = second item in command line list (first is script name)
**Plain English:** "Save the folder path the user gave us"

```python
if not os.path.isdir(folder_path):
```
**Syntax:** `if not condition:` = check if something is false
- `os.path.isdir()` = check if path is a directory
**Plain English:** "If the path isn't a real folder"

---

## Lines 46-60: File Checking

```python
print(f"Looking in {folder_path}")
```
**Syntax:** `f"text {variable}"` = f-string, puts variable inside text
**Plain English:** "Show which folder we're looking in"

```python
cr_list_file = os.path.join(folder_path, 'Models_CR_List.txt')
```
**Syntax:** `os.path.join(path1, path2)` = combine folder and filename properly
**Plain English:** "Create the full path to the CR list file"

```python
if not os.path.exists(cr_list_file):
```
**Syntax:** `os.path.exists()` = check if file exists
**Plain English:** "If the CR list file doesn't exist"

---

## Lines 62-93: Reading CR List

```python
cr_lines = []
```
**Syntax:** `variable = []` = create empty list
**Plain English:** "Make an empty list to store file lines"

```python
encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']
```
**Syntax:** `['item1', 'item2']` = create list with items
**Plain English:** "List of different text formats to try"

```python
for encoding in encodings:
```
**Syntax:** `for item in list:` = loop through each item
**Plain English:** "Try each text format one by one"

```python
try:
    with open(cr_list_file, 'r', encoding=encoding) as f:
        cr_lines = f.readlines()
    break
except:
    continue
```
**Syntax:** 
- `try:` = attempt this code
- `with open(file, mode, encoding) as variable:` = open file safely
- `f.readlines()` = read all lines into list
- `break` = exit the loop
- `except:` = if error happens
- `continue` = try next item in loop
**Plain English:** "Try to open file with this format. If it works, stop trying. If not, try next format."

```python
known_crs = set()
```
**Syntax:** `set()` = create empty set (like list but no duplicates)
**Plain English:** "Make container for unique CR numbers"

```python
cr_titles = {}
```
**Syntax:** `{}` = create empty dictionary (key-value pairs)
**Plain English:** "Make container to match CR numbers to titles"

```python
for line in cr_lines:
```
**Syntax:** `for item in list:` = go through each item
**Plain English:** "Look at each line from the file"

```python
line = line.strip()
```
**Syntax:** `.strip()` = remove spaces/newlines from start and end
**Plain English:** "Clean up the line (remove extra spaces)"

```python
if line.startswith('CR '):
```
**Syntax:** `.startswith('text')` = check if line begins with text
**Plain English:** "If line starts with 'CR '"

```python
cr_match = re.search(r'CR\s+(\w+)\s*(.*)', line)
```
**Syntax:** `re.search(pattern, text)` = find pattern in text
- `r'pattern'` = raw string (for regex patterns)
- `\s+` = one or more spaces
- `(\w+)` = capture group for word characters
- `(.*)` = capture group for everything else
**Plain English:** "Find CR number and title using pattern matching"

```python
if cr_match:
```
**Syntax:** `if variable:` = check if variable has value (not None/empty)
**Plain English:** "If pattern matching found something"

```python
cr_number = cr_match.group(1)
```
**Syntax:** `.group(number)` = get specific captured group from regex
**Plain English:** "Get the CR number part from the match"

```python
cr_normalized = cr_number.upper()
```
**Syntax:** `.upper()` = convert text to uppercase
**Plain English:** "Make CR number uppercase"

```python
if cr_normalized.isdigit():
```
**Syntax:** `.isdigit()` = check if string contains only numbers
**Plain English:** "If CR number is all digits"

```python
cr_normalized = str(int(cr_normalized))
```
**Syntax:** 
- `int(text)` = convert text to number
- `str(number)` = convert number back to text
**Plain English:** "Remove leading zeros (000123 becomes 123)"

```python
known_crs.add(cr_normalized)
```
**Syntax:** `.add(item)` = put item in set
**Plain English:** "Add this CR to our list of known CRs"

---

## Lines 95-127: Reading CR Metadata

```python
cr_full_titles = {}
```
**Syntax:** `{}` = empty dictionary
**Plain English:** "Container to store CR numbers and their full titles"

```python
if os.path.exists(cr_metadata_file):
```
**Syntax:** Same as before - check if file exists
**Plain English:** "If metadata file exists"

```python
cr_match = re.search(r'CR\s+(\w+)\s+(.*)', line)
```
**Syntax:** Same regex pattern as before
**Plain English:** "Find CR number and description"

```python
title_only = cr_match.group(2)
```
**Syntax:** `.group(2)` = get second captured group
**Plain English:** "Get just the title part (without CR number)"

```python
cr_full_titles[cr_normalized] = title_only
```
**Syntax:** `dictionary[key] = value` = store key-value pair
**Plain English:** "Link this CR number to its title"

---

## Lines 128-142: Reading Team List

```python
team_lines = []
```
**Syntax:** Empty list creation
**Plain English:** "Container for team member names"

```python
team_members = [line.strip() for line in team_lines if line.strip()]
```
**Syntax:** `[expression for item in list if condition]` = list comprehension
**Plain English:** "Take each line, clean it up, only keep non-empty ones"

---

## Lines 143-150: Finding Status Files

```python
txt_files = []
```
**Syntax:** Empty list
**Plain English:** "Container for status file paths"

```python
for file in os.listdir(folder_path):
```
**Syntax:** `os.listdir(path)` = get list of files in folder
**Plain English:** "Look at each file in the folder"

```python
if file.endswith('.txt') and not file.startswith('Models_') and file != 'CR_Metadata.txt':
```
**Syntax:** 
- `.endswith('text')` = check if filename ends with text
- `and` = all conditions must be true
- `not` = opposite of condition
- `!=` = not equal to
**Plain English:** "If file is .txt AND doesn't start with 'Models_' AND isn't the metadata file"

```python
txt_files.append(os.path.join(folder_path, file))
```
**Syntax:** `.append(item)` = add item to end of list
**Plain English:** "Add this file's full path to our list"

---

## Lines 155-200: Processing Each Person

```python
email_crs = set()
```
**Syntax:** Empty set
**Plain English:** "Container for all CRs found in status files"

```python
assignments = {}
```
**Syntax:** Empty dictionary
**Plain English:** "Container to track who worked on what"

```python
person_name = os.path.splitext(os.path.basename(txt_file))[0]
```
**Syntax:** 
- `os.path.basename(path)` = get filename from full path
- `os.path.splitext(filename)` = split filename and extension
- `[0]` = get first part (before the dot)
**Plain English:** "Get person's name from filename (remove .txt)"

```python
print(f"  {person_name}...", end=" ")
```
**Syntax:** `end=" "` = don't add newline, use space instead
**Plain English:** "Show person's name and stay on same line"

```python
content = None
```
**Syntax:** `None` = empty/null value
**Plain English:** "Start with no file content"

```python
with open(txt_file, 'r', encoding=encoding) as f:
    content = f.read()
```
**Syntax:** `.read()` = read entire file as one string
**Plain English:** "Read the whole file into memory"

```python
lines = content.split('\n')
```
**Syntax:** `.split('character')` = break string into list at character
**Plain English:** "Split file content into separate lines"

```python
line_trimmed = line.strip()
```
**Syntax:** Same as before - remove extra spaces
**Plain English:** "Clean up the line"

```python
if line_trimmed.upper().startswith('CR'):
```
**Syntax:** Chain methods together
**Plain English:** "If line starts with 'CR' (uppercase version)"

```python
line_start = line_trimmed[:15]
```
**Syntax:** `string[start:end]` = slice string (get part of it)
**Plain English:** "Get first 15 characters of the line"

```python
if re.search(r'\d', cr) or cr.upper() in ['FOD01', 'FOD02', 'A_III', 'A__II']:
```
**Syntax:** 
- `\d` = any digit
- `or` = either condition can be true
- `in [list]` = check if item exists in list
**Plain English:** "If CR has a digit OR is one of these special codes"

```python
crs_found.add(cr_normalized)
```
**Syntax:** Add to set (no duplicates)
**Plain English:** "Add this CR to person's list"

```python
email_crs.update(crs_found)
```
**Syntax:** `.update(set)` = add all items from one set to another
**Plain English:** "Add all of this person's CRs to master list"

```python
print(f"{', '.join(['CR ' + cr for cr in crs_found])}")
```
**Syntax:** 
- `', '.join(list)` = combine list items with commas
- `['CR ' + cr for cr in crs_found]` = add 'CR ' to each item
**Plain English:** "Show all CRs this person worked on, separated by commas"

---

## Lines 202-220: Finding New CRs

```python
new_crs = email_crs - known_crs
```
**Syntax:** `set1 - set2` = set difference (items in first but not second)
**Plain English:** "Find CRs that are in status files but not in known list"

```python
if new_crs:
```
**Syntax:** Check if set has items
**Plain English:** "If we found any new CRs"

```python
with open(cr_list_file, 'a', encoding='utf-8') as f:
```
**Syntax:** `'a'` = append mode (add to end of file)
**Plain English:** "Open CR list file to add new stuff"

```python
for cr in sorted(new_crs):
```
**Syntax:** `sorted(list)` = put items in alphabetical order
**Plain English:** "Go through new CRs in alphabetical order"

```python
f.write(f"\nCR {cr} [Found in status emails]")
```
**Syntax:** `\n` = newline character, `.write()` = add text to file
**Plain English:** "Add each new CR to the file on a new line"

---

## Lines 225-240: Creating Report Matrix

```python
all_crs = sorted(list(known_crs.union(email_crs)))
```
**Syntax:** 
- `.union(set)` = combine two sets
- `list()` = convert set to list
- `sorted()` = alphabetical order
**Plain English:** "Combine all known and found CRs, put in order"

```python
cr_list_for_report = ['CR ' + cr for cr in all_crs]
```
**Syntax:** List comprehension - add 'CR ' to each item
**Plain English:** "Add 'CR ' prefix to each CR number for display"

```python
matrix = {name: {cr: ' ' for cr in cr_list_for_report} for name in team_members}
```
**Syntax:** Nested dictionary comprehension
**Plain English:** "Create grid: each person has each CR set to empty space"

```python
if cr_with_prefix in cr_list_for_report:
    matrix[name][cr_with_prefix] = 'X'
```
**Syntax:** 
- `if condition:` = check first
- `dictionary[key1][key2] = value` = set nested dictionary value
**Plain English:** "If this CR is in our report, mark this person as working on it"

---

## Lines 241-263: Writing CSV

```python
with open(output_file, 'w', newline='') as csvfile:
```
**Syntax:** `'w'` = write mode, `newline=''` = proper CSV format
**Plain English:** "Create new CSV file for writing"

```python
writer = csv.writer(csvfile)
```
**Syntax:** Create CSV writer object
**Plain English:** "Set up tool to write spreadsheet format"

```python
cr_titles_row = ['TITLE']
```
**Syntax:** Start list with one item
**Plain English:** "Begin title row with 'TITLE' header"

```python
for cr_with_prefix in cr_list_for_report:
    cr_number = cr_with_prefix.replace('CR ', '')
```
**Syntax:** `.replace('old', 'new')` = substitute text
**Plain English:** "Remove 'CR ' prefix to get just the number"

```python
if cr_number in cr_full_titles:
    title = cr_full_titles[cr_number]
else:
    title = "[Title not available - found in status emails]"
```
**Syntax:** `if-else` = choose between two options
**Plain English:** "If we have a title for this CR, use it. Otherwise, use placeholder."

```python
writer.writerow(cr_titles_row)
```
**Syntax:** `.writerow(list)` = write one row to CSV
**Plain English:** "Write the title row to the spreadsheet"

```python
row = [name] + [matrix[name][cr] for cr in cr_list_for_report]
```
**Syntax:** 
- `list1 + list2` = combine lists
- List comprehension to get all CR assignments
**Plain English:** "Create row starting with name, followed by X or space for each CR"

---

## Lines 268-275: Final Summary

```python
assigned_crs = [cr for cr in cr_list_for_report if matrix[name][cr] == 'X']
```
**Syntax:** List comprehension with condition
**Plain English:** "Get list of CRs where this person has an X"

```python
if assigned_crs:
    print(f"  {name}: {', '.join(assigned_crs)}")
else:
    print(f"  {name}: none")
```
**Syntax:** if-else with different print statements
**Plain English:** "If person has assignments, show them. Otherwise, show 'none'."

---

## Line 277: Program Entry Point

```python
if __name__ == "__main__":
    main()
```
**Syntax:** Special Python check - only run if this file is executed directly
**Plain English:** "If someone runs this file directly, start the main function"

---

*Now you can explain any line of code with confidence!* 🎯
