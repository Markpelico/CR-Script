# NASA Models Team CR Support Report - Simplified Version

## What This Script Does

This script processes weekly status reports from team members and creates a matrix showing which team members worked on which Change Requests (CRs). The output is a CSV file that can be easily copied into PowerPoint for presentations.

## Key Simplifications Made

1. **Removed .eml file support** - Only processes .txt files now
2. **Eliminated complex functions** - All logic is now in one main() function
3. **Clear main section** - The main() function is clearly marked as "MAIN CODE - This is where the main logic happens"
4. **Design by Contract** - Added preconditions and postconditions for clarity
5. **Step-by-step comments** - Each major step is numbered and explained
6. **Simplified error handling** - Basic try/except blocks instead of complex encoding detection
7. **Kept Joe's changes** - Maintained the str() formatting for print statements
8. **Two header rows** - Full CR titles in row 1, just CR numbers in row 2

## How to Use

1. Place all your files in a folder:

   - `Models_CR_List.txt` - List of known CRs with full titles
   - `Models_Group.txt` - Team member names (one per line)
   - Individual status files (e.g., `Bob.txt`, `Hunter.txt`, etc.)

2. Run the script:

   ```
   python simple_script.py your_folder_name
   ```

3. The script will create `Models_CR_Worked.csv` in the same folder

## Input File Formats

### Models_CR_List.txt

```
Date 7/23/2025
CR 86193 Implementation: Artemis III Training Systems SpaceX HLS Interfaces with Orion
CR 84492 Design: CR 16397 - ISS Integration Support for the Axiom Commercial Segment Critical Design Review
...
```

### Models_Group.txt

```
Dean
Ramon
Sergio
Paula
Duncan
...
```

### Status Files (e.g., Bob.txt)

```
From: Hafernick, Robert B. (JSC-CD411)[KBR Wyle Services, LLC]
Subject: Bob Hafernick - Weekly Status

CR 84492 Design: Axiom Integration Critical Design Review (CDR)
No work

CR A__II
...
```

## Output

The script creates a CSV file with **two header rows**:

- **Row 1**: Full CR titles (e.g., "CR 86193 Implementation: Artemis III Training Systems SpaceX HLS Interfaces with Orion")
- **Row 2**: Just CR numbers (e.g., "CR 86193")
- **Data rows**: Team member names in first column, 'X' for assignments, spaces for no work

This gives you flexibility for PowerPoint presentations:

- Use Row 1 for detailed presentations to technical audiences
- Use Row 2 for high-level presentations to management

## Design by Contract

**Preconditions:**

- Folder must contain Models_CR_List.txt and Models_Group.txt
- Status files must be in .txt format

**Postconditions:**

- Creates Models_CR_Worked.csv with team assignments matrix (two header rows)
- Prints summary to console

## Example Output

```
Processing folder: txtfiles
Reading Models_CR_List.txt...
Found 21 known CRs in Models_CR_List.txt
Reading Models_Group.txt...
Found 16 team members: Dean, Ramon, Sergio, Paula, Duncan, Hunter, Jaheim, Mark, Philip, Bob, Chris, Thomas, Joe, Tony, Isaac, Luis
Found 4 status files to process
Processing Bob.txt (.txt)...
  Bob: CR 84492, CR A__II
Processing Hunter.txt (.txt)...
  Hunter: CR 000083875, CR 000087893
...

CSV File created: txtfiles\Models_CR_Worked.csv
Report includes 16 team members and 22 CRs
```

## Joe's Changes Preserved & Improved

The script maintains Joe's print statement locations while making them cleaner:

- Kept Joe's specific print statement locations (marked with "# Joe was here")
- Simplified the complex `str()` concatenations to clean f-strings
- Much easier to read and maintain

## Files

- `simple_script.py` - The simplified main script (with Joe's changes and two header rows)
- `script.py` - Original complex version (kept for reference)
- `txtfiles/` - Example data folder with sample files
