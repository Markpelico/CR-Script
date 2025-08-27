#!/usr/bin/env python3
"""
Consolidated Status Report Module

This module handles the generation of consolidated CR status reports
that group work descriptions by CR number instead of by person.

Functions:
    extract_cr_work_details(content, person_name) - Extract work descriptions for each CR
    generate_consolidated_report(folder_path, cr_work_details, cr_full_titles, team_members) - Generate formatted report
"""

import re
import os
from datetime import datetime


def extract_cr_work_details(content, person_name):
    """Extract work descriptions for each CR from a person's status file
    
    Args:
        content (str): Full text content of the status file
        person_name (str): Name of the person (for reference)
    
    Returns:
        dict: {cr_number: work_description} mapping
    """
    cr_work = {}
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if line starts with CR
        if line.upper().startswith('CR'):
            # Extract CR number
            cr_match = re.search(r'\bCR\s*([A-Za-z0-9_]+)', line, re.IGNORECASE)
            if cr_match:
                cr_number = cr_match.group(1).upper()
                
                # Normalize CR format (remove leading zeros)
                if cr_number.isdigit():
                    cr_number = str(int(cr_number))
                
                # Collect work description (lines after CR until next CR or end)
                work_lines = [line]  # Include the CR line itself
                i += 1
                
                # Collect following lines until next CR or significant break
                while i < len(lines):
                    next_line = lines[i].strip()
                    
                    # Stop if we hit another CR line
                    if next_line.upper().startswith('CR') and re.search(r'\bCR\s*([A-Za-z0-9_]+)', next_line):
                        break
                    
                    # Stop if we hit multiple blank lines (section break)
                    if not next_line:
                        blank_count = 0
                        temp_i = i
                        while temp_i < len(lines) and not lines[temp_i].strip():
                            blank_count += 1
                            temp_i += 1
                        if blank_count >= 2:  # Multiple blank lines = section break
                            break
                    
                    # Add line if it has content or is just one blank line
                    if next_line or (not next_line and len(work_lines) > 0 and work_lines[-1].strip()):
                        work_lines.append(lines[i])
                    
                    i += 1
                
                # Clean up and store work description
                work_description = '\n'.join(work_lines).strip()
                if work_description:
                    cr_work[cr_number] = work_description
                
                continue  # Don't increment i again
        
        i += 1
    
    return cr_work


def generate_consolidated_report(folder_path, cr_work_details, cr_full_titles, team_members):
    """Generate consolidated status report grouped by CR
    
    Args:
        folder_path (str): Path to output folder
        cr_work_details (dict): {cr_number: {person: work_description}}
        cr_full_titles (dict): {cr_number: full_title}
        team_members (list): List of team member names
    
    Returns:
        str: Path to generated report file
    """
    output_file = os.path.join(folder_path, 'Consolidated_Status_Report.txt')
    
    # Generate header
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    total_crs = len(cr_work_details)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header section
        f.write("=" * 65 + "\n")
        f.write("NASA Models Team - Consolidated CR Status Report\n")
        f.write(f"Generated: {current_time}\n")
        f.write("Source: Weekly Status Reports\n")
        f.write(f"Total CRs with Activity: {total_crs}\n")
        f.write(f"Team Members: {len(team_members)}\n")
        f.write("=" * 65 + "\n\n")
        f.write("This report consolidates individual status updates by CR number,\n")
        f.write("showing all team member contributions for each active CR.\n\n")
        
        # Sort CRs for consistent output
        sorted_crs = sorted(cr_work_details.keys(), key=lambda x: (x.isdigit(), int(x) if x.isdigit() else x))
        
        for cr_number in sorted_crs:
            f.write("-" * 53 + "\n\n")
            
            # CR header with title if available
            if cr_number in cr_full_titles:
                f.write(f"CR {cr_number} - {cr_full_titles[cr_number]}\n")
            else:
                f.write(f"CR {cr_number}\n")
            
            # Work details for each person
            for person_name, work_description in cr_work_details[cr_number].items():
                f.write(f"{person_name} - \n")
                # Indent the work description
                indented_work = '\n'.join('    ' + line for line in work_description.split('\n'))
                f.write(f"{indented_work}\n")
            
            f.write("\n")
        
        f.write("-" * 53 + "\n")
    
    return output_file


def validate_cr_number(cr_number):
    """Validate if a CR number should be included in reports
    
    Args:
        cr_number (str): CR number to validate
    
    Returns:
        bool: True if CR should be included
    """
    return re.search(r'\d', cr_number) or cr_number.upper() in ['FOD01', 'FOD02', 'A_III', 'A__II']


def normalize_cr_number(cr_number):
    """Normalize CR number format (remove leading zeros)
    
    Args:
        cr_number (str): Original CR number
    
    Returns:
        str: Normalized CR number
    """
    cr_normalized = cr_number.upper()
    if cr_normalized.isdigit():
        cr_normalized = str(int(cr_normalized))  # Remove leading zeros
    return cr_normalized
