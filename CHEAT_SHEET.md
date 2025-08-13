# CR Script Cheat Sheet 📋

*Simple explanations for every part of the code*

## What This Script Does
Takes team status emails (txt files) and creates a spreadsheet showing who worked on which CRs.

---

## File Structure
- **simple_script.py** - The main program
- **txtfiles/Models_CR_List.txt** - List of known CRs
- **txtfiles/Models_Group.txt** - Team member names  
- **txtfiles/CR_Metadata.txt** - CR descriptions/titles
- **txtfiles/Dean.txt, Bob.txt, etc.** - Individual status files
- **txtfiles/Models_CR_Worked.csv** - Final report (output)

---

## How to Run It
```bash
python3 simple_script.py txtfiles/
```

---

## Code Breakdown (In Order)

### 1. Setup (Lines 31-60)
**What it does:** Checks if you gave it a folder and if required files exist
**Plain English:** "Did you tell me where to look? Are the important files there?"

### 2. Read CR List (Lines 61-93)  
**What it does:** Opens Models_CR_List.txt and finds all known CRs
**Plain English:** "What CRs do we already know about?"

### 3. Get CR Titles (Lines 95-127)
**What it does:** Opens CR_Metadata.txt to get full descriptions  
**Plain English:** "What do these CRs actually do?" (for the spreadsheet header)

### 4. Read Team List (Lines 128-142)
**What it does:** Opens Models_Group.txt to get everyone's names
**Plain English:** "Who's on the team?"

### 5. Find Status Files (Lines 143-150)
**What it does:** Looks for .txt files (but skips the Models files)
**Plain English:** "Find everyone's individual status emails"

### 6. Process Each Person (Lines 155-200)
**What it does:** Opens each person's file and looks for CRs they mention
**How it works:** Only looks at lines that START with "CR" (avoids false positives)
**Plain English:** "Go through each person's email and see what CRs they worked on"

### 7. Find New CRs (Lines 202-220)
**What it does:** Compares what we found vs what we knew about
**Auto-update:** Adds new CRs to Models_CR_List.txt automatically
**Plain English:** "Did we discover any CRs we didn't know about? Add them to our list."

### 8. Create the Spreadsheet (Lines 225-263)
**What it does:** Makes a CSV with titles, CR codes, and X marks for assignments
**Format:** 
- Row 1: CR descriptions 
- Row 2: CR numbers
- Row 3+: Team members with X marks
**Plain English:** "Make the final report that's ready for PowerPoint"

---

## Key Features Explained

### CR Detection Logic (Lines 178-191)
```python
if line_trimmed.upper().startswith('CR'):
```
**What this means:** Only count CRs if they're at the start of a line
**Why:** Prevents false positives like "completed AFTER CR83875" from counting

### Leading Zero Fix (Lines 186-191)
```python
if cr_normalized.isdigit():
    cr_normalized = str(int(cr_normalized))
```
**What this means:** Turns "000087893" into "87893"  
**Why:** Keeps everything consistent

### Auto-Update (Lines 212-219)
```python
with open(cr_list_file, 'a', encoding='utf-8') as f:
    f.write(f"\nCR {cr} [Found in status emails]")
```
**What this means:** Automatically adds new CRs to the master list
**Why:** System maintains itself - no manual updates needed

---

## Common Questions & Answers

**Q: Why does it only look at the first part of each line?**  
A: To avoid counting CRs mentioned in descriptions as actual work

**Q: What if someone's file can't be read?**  
A: Script tries multiple text formats, skips if it can't read, keeps going

**Q: What happens to new CRs?**  
A: They get added to Models_CR_List.txt automatically and show up in reports

**Q: Why two header rows?**  
A: Top row has full descriptions, bottom row has CR numbers - looks professional in PowerPoint

**Q: What if CR_Metadata.txt is missing?**  
A: Script still works, just uses placeholder titles like "[Title not available]"

---

## Error Messages Explained

- **"couldn't read"** - File encoding issue, script continues
- **"none"** - Person has no CRs in their status  
- **"No metadata file found"** - CR_Metadata.txt missing, uses placeholders
- **"Couldn't update file"** - Permission issue, report still works

---

## Output Explained

**During run:**
```
Looking in txtfiles/
Reading CR list...
Found 21 CRs
  Dean... CR 83200, CR 86343, CR 86400
New: CR 86400
Adding to CR list...
Done
```

**What each line means:**
- Shows progress through each step
- Lists what CRs each person worked on
- Shows any newly discovered CRs
- Confirms updates were saved

---

## Pro Tips 💡

1. **The script is self-maintaining** - just run it, it handles the rest
2. **It's designed to not break** - lots of error handling built in  
3. **Output is PowerPoint-ready** - just open the CSV and copy/paste
4. **New team members?** - Just add their .txt file to the folder
5. **New CRs?** - Script finds and adds them automatically

---

*Keep this handy for any questions about how the code works!*
