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
import argparse
from datetime import datetime
from consolidated_report import extract_cr_work_details, generate_consolidated_report, validate_cr_number, normalize_cr_number

def main():
    """MAIN CODE - This is where the main logic happens"""
    
    # PRECONDITION: Parse command line arguments
    parser = argparse.ArgumentParser(description='NASA Models Team CR Support Report')
    parser.add_argument('folder_path', help='Path to folder containing status files')
    parser.add_argument('--consolidated', action='store_true', 
                       help='Generate consolidated status report (groups work by CR)')
    
    args = parser.parse_args()
    folder_path = args.folder_path
    
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory")
        sys.exit(1)
    
    print(f"Looking in {folder_path}")
    
    # PRECONDITION: Check required files exist
    cr_list_file = os.path.join(folder_path, 'Models_CR_List.txt')
    team_file = os.path.join(folder_path, 'Models_Group.txt')
    cr_metadata_file = os.path.join(folder_path, 'CR_Metadata.txt')
    
    if not os.path.exists(cr_list_file):
        print(f"Error: Models_CR_List.txt not found in {folder_path}")
        sys.exit(1)
    
    if not os.path.exists(team_file):
        print(f"Error: Models_Group.txt not found in {folder_path}")
        sys.exit(1)
    
    # STEP 1: Read CR list with full titles
    print("Reading CR list...")
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
                # Normalize CR format using module function
                cr_normalized = normalize_cr_number(cr_number)
                full_title = line  # Keep the full line as title
                known_crs.add(cr_normalized)
                cr_titles[cr_normalized] = full_title
    
    print(f"Found {len(known_crs)} CRs")
    
    # STEP 1.5: Read CR metadata for titles
    print("Getting titles...")
    cr_full_titles = {}  # {cr_number: title_without_cr_prefix}
    
    if os.path.exists(cr_metadata_file):
        # Try multiple encodings for metadata file
        metadata_lines = []
        for encoding in encodings:
            try:
                with open(cr_metadata_file, 'r', encoding=encoding) as f:
                    metadata_lines = f.readlines()
                break
            except:
                continue
        
        for line in metadata_lines:
            line = line.strip()
            if line.startswith('CR '):
                # Extract CR number and title (remove CR prefix)
                cr_match = re.search(r'CR\s+(\w+)\s+(.*)', line)
                if cr_match:
                    cr_number = cr_match.group(1)
                    title_only = cr_match.group(2)  # Just the title part, no CR number
                    # Normalize CR number format using module function
                    cr_normalized = normalize_cr_number(cr_number)
                    cr_full_titles[cr_normalized] = title_only
        
        print(f"Got {len(cr_full_titles)} titles")
    else:
        print("No metadata file found")
    
    # STEP 2: Read team member names
    print("Reading team list...")
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
    print(f"Team: {', '.join(team_members)}")
    
    # STEP 3: Find all .txt files (excluding the Models files, CR_Metadata, and generated reports)
    txt_files = []
    for file in os.listdir(folder_path):
        if (file.endswith('.txt') and 
            not file.startswith('Models_') and 
            file != 'CR_Metadata.txt' and 
            file != 'Consolidated_Status_Report.txt'):
            txt_files.append(os.path.join(folder_path, file))
    
    print(f"Processing {len(txt_files)} status files...")
    
    # STEP 4: Process status files to find CRs and assignments
    email_crs = set()  # All CRs found in status files
    assignments = {}   # {name: set of CRs they worked on}
    cr_work_details = {}  # {cr_number: {person: work_description}} for consolidated report
    
    for txt_file in txt_files:
        person_name = os.path.splitext(os.path.basename(txt_file))[0]
        print(f"  {person_name}...", end=" ")
        
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
            print("couldn't read")
            continue
        
        # Find CRs mentioned in this file (only from lines that START with CR)
        crs_found = set()
        
        # Extract work details if consolidated report is requested
        if args.consolidated:
            person_cr_work = extract_cr_work_details(content, person_name)
            for cr_number, work_desc in person_cr_work.items():
                if validate_cr_number(cr_number):
                    crs_found.add(cr_number)
                    # Store work details for consolidated report
                    if cr_number not in cr_work_details:
                        cr_work_details[cr_number] = {}
                    cr_work_details[cr_number][person_name] = work_desc
        
        # Original CR detection (for CSV report)
        lines = content.split('\n')
        for line in lines:
            # Only process lines that start with CR (after trimming whitespace)
            line_trimmed = line.strip()
            if line_trimmed.upper().startswith('CR'):
                # Only check the first 15 characters to avoid duplicate matches in same line
                line_start = line_trimmed[:15]
                cr_matches = re.findall(r'\bCR\s*([A-Za-z0-9_]+)', line_start, re.IGNORECASE)
                for cr in cr_matches:
                    if validate_cr_number(cr):
                        # Normalize CR format using module function
                        cr_normalized = normalize_cr_number(cr)
                        crs_found.add(cr_normalized)
        
        email_crs.update(crs_found)
        
        if crs_found:
            assignments[person_name] = crs_found
            print(f"{', '.join(['CR ' + cr for cr in crs_found])}")
        else:
            assignments[person_name] = set()
            print("none")
    
    # STEP 5: Find new CRs that weren't in the original list
    new_crs = email_crs - known_crs
    if new_crs:
        print(f"\nNew: {', '.join(['CR ' + cr for cr in new_crs])}")
        # Add new CRs to titles with placeholder
        for cr in new_crs:
            cr_titles[cr] = f"CR {cr} [Found in status emails]"
        
        # STEP 5.1: Append new CRs to Models_CR_List.txt for future runs
        print("Adding to CR list...")
        try:
            with open(cr_list_file, 'a', encoding='utf-8') as f:
                for cr in sorted(new_crs):  # Sort for consistent ordering
                    f.write(f"\nCR {cr} [Found in status emails]")
            print("Done")
        except Exception as e:
            print(f"Couldn't update file: {e}")
            print("(Report will still work)")
    
    # STEP 6: Create union of all CRs (known + discovered)
    all_crs = sorted(list(known_crs.union(email_crs)))
    cr_list_for_report = ['CR ' + cr for cr in all_crs]
    
    print(f"\nGenerating report with {len(cr_list_for_report)} CRs...")
    
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
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write title row (first row with just titles, no CR numbers)
        cr_titles_row = ['TITLE']
        for cr_with_prefix in cr_list_for_report:
            cr_number = cr_with_prefix.replace('CR ', '')  # Remove 'CR ' prefix
            if cr_number in cr_full_titles:
                title = cr_full_titles[cr_number]
            else:
                title = "[Title not available - found in status emails]"
            cr_titles_row.append(title)
        writer.writerow(cr_titles_row)
        
        # Write CR numbers row (second row)
        cr_numbers = ['NAME'] + cr_list_for_report
        writer.writerow(cr_numbers)
        
        # Write data rows (team members)
        for name in team_members:
            row = [name] + [matrix[name][cr] for cr in cr_list_for_report]
            writer.writerow(row)
    
    # POSTCONDITION: Report completion
    print(f"Saved: {output_file}")
    
    # Generate consolidated report if requested
    if args.consolidated:
        if cr_work_details:
            print("Generating consolidated report...")
            report_file = generate_consolidated_report(folder_path, cr_work_details, cr_full_titles, team_members)
            print(f"Consolidated report saved: {report_file}")
        else:
            print("No CR work details found for consolidated report")
    
    # Print summary
    print("\nSummary:")
    for name in team_members:
        assigned_crs = [cr for cr in cr_list_for_report if matrix[name][cr] == 'X']
        if assigned_crs:
            print(f"  {name}: {', '.join(assigned_crs)}")
        else:
            print(f"  {name}: none")

if __name__ == "__main__":
    main() 