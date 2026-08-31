#!/usr/bin/env python3
import os
import re
from collections import defaultdict

def split_camel_case(name):
    """Split camelCase into space-separated words."""
    # Insert space before uppercase letters that follow lowercase letters
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    # Insert space before uppercase letters that follow uppercase letters followed by lowercase
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', name)
    return name

def clean_name(filename, is_fajr=False):
    """Clean the filename to extract the caller name."""
    # Remove .mp3 extension
    name = filename.replace('.mp3', '')
    
    # Remove number prefixes like "1-", "10-"
    name = re.sub(r'^\d+-', '', name)
    
    # For fajr files, remove Adhan-Al-Fajr and related suffixes
    if is_fajr:
        # Remove patterns like -Adhan-Al-Fajr-Misr, -Adhan-Fajr-Al-Kuwait, etc.
        name = re.sub(r'-?Adhan-?Al-?Fajr.*$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'-?Adhan-?Fajr.*$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'-?Fajr.*$', '', name, flags=re.IGNORECASE)
    
    # For location-based files starting with "Adhan"
    if name.startswith('Adhan'):
        # Remove "Adhan" prefix and extract location
        name = re.sub(r'^Adhan-?', '', name, flags=re.IGNORECASE)
        # Remove "From" prefix if present
        name = re.sub(r'^From-?', '', name, flags=re.IGNORECASE)
        # Remove "With" prefix if present
        name = re.sub(r'^With-?', '', name, flags=re.IGNORECASE)
    
    # Remove descriptive suffixes (location, year, makam info)
    suffixes_to_remove = [
        r'-sultanahmetMosque.*$',
        r'-mescidiEmevi.*$',
        r'-mescidiEzher.*$',
        r'-mescidiNebevi.*$',
        r'-mescidiAksa.*$',
        r'-turkiye.*$',
        r'-suriye.*$',
        r'-syria.*$',
        r'-bornovaMerkez.*$',
        r'-19\d{2}.*$',
        r'-20\d{2}.*$',
        r'-cut$',
        r'-sonundakiEzan.*$',
        r'-baghdadRadio.*$',
        r'-nihavendMakami.*$',
        r'-rastMakami.*$',
        r'-acemMakami.*$',
        r'-sabaMakami.*$',
        r'-sigaMakami.*$',
        r'-bayatMakami.*$',
        r'-hicazMakami.*$',
        r'-hicazMakam.*$',
        r'-kurdiMakami.*$',
        r'-veSela.*$',
        r'-libya.*$',
        r'-iraq.*$',
        r'-jazaer.*$',
        r'-kuwait.*$',
        r'-qahera.*$',
        r'-ummAlQuwain.*$',
        r'-doaa$',
        r'-withDoaa$',
        r'Ezan$',
        r'Ezan_.*$',
        r'Adhan$',
    ]
    
    for pattern in suffixes_to_remove:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    
    # Remove remaining hyphens and replace with spaces
    name = name.replace('-', ' ')
    # Remove underscores and replace with spaces
    name = name.replace('_', ' ')
    
    # Split camelCase
    name = split_camel_case(name)
    
    # Clean up multiple spaces
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Remove trailing numbers that might have been left
    name = re.sub(r'\s+\d+$', '', name)
    
    # Fix common issues
    # Fix "mustafaIsmail" -> "Mustafa Ismail"
    name = re.sub(r'mustafaIsmail', 'Mustafa Ismail', name, flags=re.IGNORECASE)
    # Fix "Abdussamedfrom" -> "Abdussamed"
    name = re.sub(r'Abdussamedfrom.*', 'Abdussamed', name)
    # Fix "MuhammedSeyyidHasaneynfather" -> "Muhammed Seyyid Hasaneyn"
    name = re.sub(r'MuhammedSeyyidHasaneynfather.*', 'Muhammed Seyyid Hasaneyn', name)
    # Fix "Muhammmed" -> "Muhammed"
    name = name.replace('Muhammmed', 'Muhammed')
    # Fix "Albaniaarnavut" -> "Albania"
    name = re.sub(r'Albaniaarnavut.*', 'Albania', name)
    # Fix "Algeria Adhan" -> "Algeria"
    name = re.sub(r'Algeria Adhan', 'Algeria', name)
    # Fix "Jerusalem Adhan" -> "Jerusalem"
    name = re.sub(r'Jerusalem Adhan', 'Jerusalem', name)
    # Fix "Malaysia Adhan" -> "Malaysia"
    name = re.sub(r'Malaysia Adhan', 'Malaysia', name)
    # Fix "Syria Adhan" -> "Syria"
    name = re.sub(r'Syria Adhan', 'Syria', name)
    # Fix "Iran Ezan" -> "Iran"
    name = re.sub(r'Iran Ezan', 'Iran', name)
    # Fix "Turk Ezan" -> "Turk"
    name = re.sub(r'Turk Ezan', 'Turk', name)
    # Fix "Birecik Ezanfevzi Polat" -> "Birecik Fevzi Polat"
    name = re.sub(r'Birecik Ezanfevzi Polat', 'Birecik Fevzi Polat', name)
    # Fix "Ahmed Naina_ishak Dan_ezan" -> "Ahmed Naina"
    name = re.sub(r'Ahmed Naina.*', 'Ahmed Naina', name)
    # Fix "Ahmed abdu Rahman Darar" -> "Ahmed Abdurahman Darar"
    name = name.replace('Ahmed abdu Rahman Darar', 'Ahmed Abdurahman Darar')
    # Fix "Ibraheem jabr Abu Raheq" -> "Ibraheem Jabr Abu Raheq"
    name = name.replace('Ibraheem jabr Abu Raheq', 'Ibraheem Jabr Abu Raheq')
    # Fix "Muhammed Imran sabah" -> "Muhammed Imran"
    name = re.sub(r'Muhammed Imran sabah.*', 'Muhammed Imran', name)
    # Fix "With Ney" -> "Ney"
    name = re.sub(r'With Ney', 'Ney', name)
    # Fix "Ney.mp3" -> "Ney.mp3"
    name = re.sub(r'^Ney$', 'Ney', name)
    
    # Handle location-based files that start with "Al" or "Umm" etc.
    # These should keep the location name
    if name.startswith('Al') or name.startswith('Umm'):
        # Keep as is
        pass
    
    # Handle empty names - use the original filename
    if not name or name == '.' or name.startswith('-'):
        # Use the original filename without extension
        name = filename.replace('.mp3', '')
        # Remove number prefixes
        name = re.sub(r'^\d+-', '', name)
        # Replace hyphens with spaces
        name = name.replace('-', ' ')
        # Split camelCase
        name = split_camel_case(name)
    
    return name

def get_files(directory):
    """Get all mp3 files in a directory."""
    files = []
    for f in os.listdir(directory):
        if f.endswith('.mp3'):
            files.append(f)
    return sorted(files)

def rename_files(directory, is_fajr=False):
    """Rename files in a directory."""
    files = get_files(directory)
    name_count = defaultdict(int)
    renames = []
    
    for filename in files:
        new_name = clean_name(filename, is_fajr)
        
        # Handle duplicates
        base_name = new_name
        if name_count[new_name] > 0:
            new_name = f"{base_name}-{name_count[new_name] + 1}"
        name_count[base_name] += 1
        
        new_filename = f"{new_name}.mp3"
        renames.append((filename, new_filename))
        
        # Rename the file
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        
        if old_path != new_path:
            print(f"Renaming: {filename} -> {new_filename}")
            os.rename(old_path, new_path)
        else:
            print(f"No change: {filename}")
    
    return renames

def update_html(html_path, renames):
    """Update the index.html file with new filenames."""
    with open(html_path, 'r') as f:
        content = f.read()
    
    for old_name, new_name in renames:
        content = content.replace(f'"{old_name}"', f'"{new_name}"')
    
    with open(html_path, 'w') as f:
        f.write(content)
    
    print(f"Updated {html_path}")

# Process Shia directory
print("=== Processing Shia Directory ===")
shia_dir = '/Users/skander.jabouzi/Development/KMP/jabouzi.github.io/salat/adhan/shia'
shia_renames = rename_files(shia_dir, is_fajr=False)
update_html(os.path.join(shia_dir, 'index.html'), shia_renames)

# Process Sunnah Fajr directory
print("\n=== Processing Sunnah Fajr Directory ===")
fajr_dir = '/Users/skander.jabouzi/Development/KMP/jabouzi.github.io/salat/adhan/sunnah/fajr'
fajr_renames = rename_files(fajr_dir, is_fajr=True)
update_html(os.path.join(fajr_dir, 'index.html'), fajr_renames)

# Process Sunnah Other directory
print("\n=== Processing Sunnah Other Directory ===")
other_dir = '/Users/skander.jabouzi/Development/KMP/jabouzi.github.io/salat/adhan/sunnah/other'
other_renames = rename_files(other_dir, is_fajr=False)
update_html(os.path.join(other_dir, 'index.html'), other_renames)

print("\n=== Renaming Complete ===")
print(f"Shia: {len(shia_renames)} files")
print(f"Fajr: {len(fajr_renames)} files")
print(f"Other: {len(other_renames)} files")
