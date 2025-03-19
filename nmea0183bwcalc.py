#!/usr/bin/env python3

import json
import os
from pathlib import Path

def load_database():
    """Load NMEA sentence database from JSON"""
    try:
        db_path = Path(__file__).parent / 'nmea_sentences.json'
        with open(db_path, 'r') as f:
            data = json.load(f)
        return data['sentences']
    except Exception as e:
        print(f"Error loading database: {str(e)}")
        return {}

def clear():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def printMenu():
    """Print the main menu."""
    print("\nNMEA 0183 Bandwidth Calculator")
    print("1. Show sentence details")
    print("2. Calculate bandwidth")
    print("3. Show Help")
    print("4. Exit")
    print("\nEnter your choice (1-4):", end=" ")

def printSentenceList(database):
    """Print available sentence IDs in a grid format."""
    sentences = sorted(list(database.keys()))
    num_cols = 8
    num_rows = (len(sentences) + num_cols - 1) // num_cols
    col_width = 6

    print("\nAvailable NMEA 0183 Sentences:")
    print("-" * (col_width * num_cols))

    for row in range(num_rows):
        row_items = []
        for col in range(num_cols):
            idx = row + (col * num_rows)
            if idx < len(sentences):
                row_items.append(f"{sentences[idx]:<{col_width}}")
        print("".join(row_items))
    print("-" * (col_width * num_cols))

def showSentenceDetails(database):
    """Show comprehensive details of a specified sentence."""
    clear()
    print("\nShow Sentence Details")
    printSentenceList(database)
    print("\nEnter sentence ID (or 'q' to return to menu):", end=" ")
    
    while True:
        ID = input().upper()
        if ID == 'Q':
            return
        try:
            sentence = database[ID]
            print(f"\n{'-'*50}")
            print(f"{ID} is {len(sentence['sentence_structure'])} bytes long")
            print(f"Description: {sentence['sentence_name']}")
            
            # Sentence structure - moved up after description
            print("\nSentence Structure:")
            print(f"  {sentence['sentence_structure']}")  # Fixed structure display
            
            # Field information
            print(f"\nNumber of Fields: {sentence['num_fields']}")
            print("\nField Details:")
            for i, (name, length) in enumerate(zip(sentence['field_names'], 
                                                 sentence['chars_per_field'])):
                print(f"  Field {i+1}: {name}, {length}")  # Name and length on same line
            
            # Standard and version information - moved to bottom
            print("\nStandard Information:")
            if sentence['standard'] == 'N':
                print("  Standard: NMEA 0183")
                if sentence['version']['nmea']:
                    print(f"  First Version: {sentence['version']['nmea'][0]}")
                    if sentence['version']['nmea'][1]:
                        print(f"  Current Version: {sentence['version']['nmea'][1]}")
            elif sentence['standard'] == 'I':
                print("  Standard: IEC 61162-1")
                if sentence['version']['iec']:
                    print(f"  Current Version: {sentence['version']['iec']}")
            elif sentence['standard'] == 'B':
                print("  Standards: NMEA 0183 and IEC 61162-1")
                if sentence['version']['nmea']:
                    print(f"  First NMEA Version: {sentence['version']['nmea'][0]}")
                    print(f"  Current NMEA Version: {sentence['version']['nmea'][1]}")
                if sentence['version']['iec']:
                    print(f"  Current IEC Version: {sentence['version']['iec']}")
            
            print(f"\n{'-'*50}")
            print("\nEnter another sentence ID (or 'q' to return to menu):", end=" ")
        except KeyError:
            print(f"Error: Sentence ID '{ID}' not found in database")
            print("\nEnter sentence ID (or 'q' to return to menu):", end=" ")

def showHelp():
    """Display help documentation from markdown file."""
    clear()
    try:
        help_path = Path(__file__).parent / 'console_help.md'
        with open(help_path, 'r') as f:
            help_text = f.read()
        print(help_text)
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"Error loading help file: {str(e)}")
        input("\nPress Enter to continue...")

def calculateBandwidth(database):
    """Calculate bandwidth usage for specified sentences."""
    sentences = []  # Move sentences list outside the rate selection loop
    
    while True:
        clear()
        print("\nCalculate Bandwidth")
        
        # Get baud rate
        print("\nSelect baud rate:")
        print("1. 4800")
        print("2. 38400")
        while True:
            choice = input("Enter choice (1-2): ")
            if choice == '1':
                baud = 4800
                break
            elif choice == '2':
                baud = 38400
                break
            print("Invalid choice")
        
        # Get update rate
        print("\nSelect update rate:")
        print("1. 2 seconds (0.5Hz)")
        print("2. 1 second (1Hz)")
        print("3. 0.5 seconds (2Hz)")
        print("4. 0.2 seconds (5Hz)")
        print("5. 0.1 seconds (10Hz)")
        print("6. 0.05 seconds (20Hz)")
        
        while True:
            choice = input("Enter choice (1-6): ")
            if choice in ['1','2','3','4','5','6']:
                periods = [2.0, 1.0, 0.5, 0.2, 0.1, 0.05]
                period = periods[int(choice)-1]
                break
            print("Invalid choice")
        
        while True:
            clear()
            print("\nCalculate Bandwidth")
            print(f"\nCurrent Settings:")
            print(f"  Baud Rate: {baud}")
            print(f"  Update Rate: {period} seconds ({1/period:.1f}Hz)")
            print("\nAvailable Sentences:")
            printSentenceList(database)
            
            # Show current selections and bandwidth first
            if sentences:
                total_bytes = sum(length for _, length in sentences)
                transmission_time = (total_bytes * 10) / baud
                bandwidth_percentage = (transmission_time / period) * 100
                
                print("\nSelected Sentences:")
                for ID, length in sentences:
                    print(f"  {ID}: {length} bytes")
                print(f"  Total: {total_bytes} bytes")
                print("\nBandwidth Usage:")
                print(create_progress_bar(bandwidth_percentage))
                if bandwidth_percentage > 100:
                    print("WARNING: Bandwidth exceeds maximum!")
                elif bandwidth_percentage > 80:
                    print("CAUTION: Bandwidth usage is high")
            
            print("\nCommands:")
            print("  Enter sentence ID to add")
            print("  'r' to reset selections")
            print("  'b' to change baud/update rates")
            print("  'c' to calculate final results")
            print("  'q' to return to menu")
            
            cmd = input("\nEnter command: ").upper()
            if cmd == 'Q':
                return
            elif cmd == 'R':
                sentences = []  # Reset selections
                continue
            elif cmd == 'B':
                break  # Go back to baud/update rate selection, keeping sentences
            elif cmd == 'C':
                if not sentences:
                    print("No sentences selected")
                    input("Press Enter to continue...")
                    continue
                
                # Show final results
                clear()
                print("\nFinal Results:")
                print(f"\nCurrent Settings:")
                print(f"  Baud Rate: {baud}")
                print(f"  Update Rate: {period} seconds ({1/period:.1f}Hz)")
                print("\nSelected Sentences:")
                for ID, length in sentences:
                    print(f"  {ID}: {length} bytes")
                print(f"  Total: {total_bytes} bytes")
                print(f"\nTransmission time: {transmission_time:.6f} seconds")
                print("\nBandwidth Usage:")
                print(create_progress_bar(bandwidth_percentage))
                if bandwidth_percentage > 100:
                    print("WARNING: Bandwidth exceeds maximum!")
                elif bandwidth_percentage > 80:
                    print("CAUTION: Bandwidth usage is high")
                input("\nPress Enter to continue...")
                return
            
            # Process sentence ID
            try:
                structure = database[cmd]['sentence_structure']
                length = len(structure)
                sentences.append((cmd, length))
                print(f"Added {cmd} ({length} bytes)")
                input("Press Enter to continue...")
            except KeyError:
                if cmd not in ['Q', 'R', 'B', 'C']:
                    print(f"Error: Sentence ID '{cmd}' not found in database")
                    input("Press Enter to continue...")

def create_progress_bar(percentage, width=50):
    """Create a console-friendly progress bar."""
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)
    color = ''
    reset = '\033[0m'
    if percentage > 100:
        color = '\033[91m'  # Red
        filled = width  # Ensure bar is completely filled when over 100%
    elif percentage > 80:
        color = '\033[93m'  # Yellow
    else:
        color = '\033[92m'  # Green
    return f"{color}[{bar}] {percentage:.1f}%{reset}"

def main():
    """Main program loop."""
    database = load_database()
    if not database:
        print("Error: Could not load NMEA sentence database")
        return
        
    while True:
        clear()
        printMenu()
        choice = input()
        if choice == '1':
            showSentenceDetails(database)
        elif choice == '2':
            calculateBandwidth(database)
        elif choice == '3':
            showHelp()
        elif choice == '4':
            break
        else:
            input("Invalid choice. Press Enter to continue...")

if __name__ == "__main__":
    main()