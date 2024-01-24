#!/usr/bin/env python3

import os
import subprocess
import argparse

def process_gitignore(gitignore_path):
    # Function to process the .gitignore file
    with open(gitignore_path, 'r') as filenames:
        lines_processed = 0
        for file in filenames:
            file = file.strip()

            # Process the files that are not comments
            if file and not file.startswith('#'):
                full_path = os.path.join(gitignore_path, file)
                
                # Check if it's a directory
                if os.path.isdir(full_path):
                    # It's a directory, use the recursive option
                    command = ["git", "rm", "--cached", "-r", file]
                else:
                    # It's a file, no need for the recursive option
                    command = ["git", "rm", "--cached", file]

                try: 
                    subprocess.run(command)
                    print(f"{file} has been successfully removed from tracking.")
                    lines_processed += 1
                except subprocess.CalledProcessError as e:
                    print(f"An error occurred while removing {file} from tracking.")
        
        if lines_processed == 0:
            filenames.close()
            print("The .gitignore file is empty or only contains comments.")

def main():
    parser = argparse.ArgumentParser(description='Process .gitignore and untrack files.')
    parser.add_argument('path', help='Path to the directory or the .gitignore file')
    
    args = parser.parse_args()

    input_path = args.path

    # If input path is a directory add .gitignore
    if os.path.isdir(input_path):
        gitignore_path = os.path.join(input_path, '.gitignore')

    # Ensure file is a .gitignore 
    elif os.path.isfile(input_path) and input_path.endswith('.gitignore'):
        gitignore_path = input_path

    else:
        parser.error("ABORTING: The file provided is not .gitignore")

    # Run the function
    if os.path.exists(gitignore_path):
        process_gitignore(gitignore_path)
    else:
        parser.error("ERROR: .gitignore file not found. Check your Directory...")

if __name__ == "__main__":
    main()