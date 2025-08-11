#!/usr/bin/env python3
"""
NASA Models Team CR Support Report - Simple Version

DESIGN BY CONTRACT:
    PRECONDITION: Folder must contain Models_CR_List.txt and Models_Group.txt
    POSTCONDITION: Creates Models_CR_Worked.csv with team assignments matrix

USAGE:
    python simple_script.py <folder_path>
    
    Example: python simple_script.py txtfiles/

INPUTS:
    - Models_CR_List.txt: List of known CRs with dates and titles
    - Models_Group.txt: Team member names, one per line  
    - *.txt files: Individual status emails (text format only)

OUTPUTS:
    - Models_CR_Worked.csv: PowerPoint-ready matrix with two header rows
        Row 1: Full CR titles (e.g., "CR 86193 Implementation: Artemis III Training Systems...")
        Row 2: Just CR numbers (e.g., "CR 86193")
    - Console summary: Assignment breakdown for verification
"""

import os
import csv
import sys
import re

def main():
    """MAIN CODE - This is where the main logic happens"""
    
    # PRECONDITION: Check command line arguments
    if len(sys.argv) < 2:
        print("Error: Please provide folder path")
        print("Usage: python simple_script.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory")
        sys.exit(1)
    
    print(f"Processing folder: {folder_path}")
    
    # PRECONDITION: Check required files exist
    cr_list_file = os.path.join(folder_path, 'Models_CR_List.txt')
    team_file = os.path.join(folder_path, 'Models_Group.txt')
    
    if not os.path.exists(cr_list_file):
        print(f"Error: Models_CR_List.txt not found in {folder_path}")
        sys.exit(1)
    
    if not os.path.exists(team_file):
        print(f"Error: Models_Group.txt not found in {folder_path}")
        sys.exit(1)
    
    # STEP 1: Read CR list with full titles
    print("Reading Models_CR_List.txt...")
    # Try multiple encodings for CR list
    cr_lines = []
    encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']
    for encoding in encodings:
        try:
            with open(cr_list_file, 'r', encoding=encoding) as f:
                cr_lines = f.readlines()
            break
        except:
            continue
    
    # Extract CR codes and full titles from file
    known_crs = set()
    cr_titles = {}  # {cr_number: full_title}
    
    for line in cr_lines:
        line = line.strip()
        if line.startswith('CR '):
            # Extract CR number and full title
            cr_match = re.search(r'CR\s+(\w+)\s*(.*)', line)
            if cr_match:
                cr_number = cr_match.group(1)
                full_title = line  # Keep the full line as title
                known_crs.add(cr_number)
                cr_titles[cr_number] = full_title
    
    print(f"Found {len(known_crs)} known CRs in Models_CR_List.txt")
    
    # STEP 2: Read team member names
    print("Reading Models_Group.txt...")
    # Try multiple encodings for team file
    team_lines = []
    for encoding in encodings:
        try:
            with open(team_file, 'r', encoding=encoding) as f:
                team_lines = f.readlines()
            break
        except:
            continue
    
    team_members = [line.strip() for line in team_lines if line.strip()]
    # Joe was here
    print(f"Found {len(team_members)} team members: {', '.join(team_members)}")
    
    # STEP 3: Find all .txt files (excluding the Models files)
    txt_files = []
    for file in os.listdir(folder_path):
        if file.endswith('.txt') and not file.startswith('Models_'):
            txt_files.append(os.path.join(folder_path, file))
    
    # Joe was here
    print(f"Found {len(txt_files)} status files to process")
    
    # STEP 4: Process status files to find CRs and assignments
    email_crs = set()  # All CRs found in status files
    assignments = {}   # {name: set of CRs they worked on}
    
    for txt_file in txt_files:
        person_name = os.path.splitext(os.path.basename(txt_file))[0]
        # Joe was here
        print(f"Processing {os.path.basename(txt_file)} (.txt)...")
        
        # Read file content with multiple encoding attempts
        content = None
        encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(txt_file, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except:
                continue
        
        if not content:
            print(f"  Warning: Could not read {txt_file}")
            continue
        
        # Find CRs mentioned in this file
        crs_found = set()
        cr_matches = re.findall(r'\bCR\s*([A-Za-z0-9_]+)', content, re.IGNORECASE)
        for cr in cr_matches:
            if re.search(r'\d', cr) or cr.upper() in ['FOD01', 'FOD02', 'A_III', 'A__II']:
                crs_found.add(cr.upper())
        
        email_crs.update(crs_found)
        
        if crs_found:
            assignments[person_name] = crs_found
            print(f"  {person_name}: {', '.join(['CR ' + cr for cr in crs_found])}")
        else:
            assignments[person_name] = set()
            print(f"  {person_name}: No CRs found")
    
    # STEP 5: Find new CRs that weren't in the original list
    new_crs = email_crs - known_crs
    if new_crs:
        print(f"\nDiscovered new CRs in status files: {', '.join(['CR ' + cr for cr in new_crs])}")
        # Add new CRs to titles with placeholder
        for cr in new_crs:
            cr_titles[cr] = f"CR {cr} [Found in status emails]"
    
    # STEP 6: Create union of all CRs (known + discovered)
    all_crs = sorted(list(known_crs.union(email_crs)))
    cr_list_for_report = ['CR ' + cr for cr in all_crs]
    
    print(f"\nTotal CRs to include in report: {len(cr_list_for_report)}")
    
    # STEP 7: Initialize matrix
    matrix = {name: {cr: ' ' for cr in cr_list_for_report} for name in team_members}
    
    # STEP 8: Fill matrix based on assignments found in status files
    for name in team_members:
        if name in assignments:
            for cr_code in assignments[name]:
                cr_with_prefix = 'CR ' + cr_code
                if cr_with_prefix in cr_list_for_report:
                    matrix[name][cr_with_prefix] = 'X'
    
    # STEP 9: Write CSV file with clean header
    output_file = os.path.join(folder_path, 'Models_CR_Worked.csv')
    print(f"\nGenerating CSV report: {output_file}")
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header row with just CR numbers (clean and simple)
        cr_numbers = ['NAME'] + cr_list_for_report
        writer.writerow(cr_numbers)
        
        # Write data rows
        for name in team_members:
            row = [name] + [matrix[name][cr] for cr in cr_list_for_report]
            writer.writerow(row)
    
    # POSTCONDITION: Report completion
    print(f"\nCSV File created: {output_file}")
    print(f"Report includes {len(team_members)} team members and {len(cr_list_for_report)} CRs")
    
    # Print summary
    print("\nAssignment Summary:")
    for name in team_members:
        assigned_crs = [cr for cr in cr_list_for_report if matrix[name][cr] == 'X']
        if assigned_crs:
            print(f"  {name}: {', '.join(assigned_crs)}")
        else:
            print(f"  {name}: No assignments found")

if __name__ == "__main__":
    main() 