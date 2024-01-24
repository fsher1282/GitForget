import os
import subprocess
import argparse

def process_gitignore(gitignore_path):
    # Function to process the .gitignore file
    with open(gitignore_path, 'r') as filenames:
        for file in filenames:
            file = file.strip()
            if file and not file.startswith('#'):
                try: 
                    subprocess.run(["git", "rm", "--cached", file], check=True)
                    print(f"File {file} has been successfully removed from tracking.")
                except subprocess.CalledProcessError as e:
                    print(f"An error occurred while removing {file} from tracking.")

def main():
    parser = argparse.ArgumentParser(description='Process .gitignore and untrack files.')
    parser.add_argument('path', help='Path to the directory or the .gitignore file')
    
    args = parser.parse_args()

    input_path = args.path

    # If input path is a directory add .gitognore
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
        parser.error("ERROR: .gitignore file not found")

if __name__ == "__main__":
    main()