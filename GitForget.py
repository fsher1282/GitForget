#!/usr/bin/env python3

import os
import subprocess
import argparse

def get_tracked_files(repo_root_path):

    # Run the git ls-files command to get a list of tracked files
    tracked_files_process = subprocess.run(
        ["git", "ls-tree", "-t", "--name-only", "HEAD"],
        cwd=repo_root_path, 
        check=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )

    # Split the output into a list of file paths
    file_paths = tracked_files_process.stdout.strip().split('\n')

    # Dictionary to store the file type (file or dir)
    tracked_file_hash = {}

    for file_path in file_paths:
        # Check if the path is a directory or a file
        if os.path.isdir(file_path):
            tracked_file_hash[file_path] = 'directory'
        else:
            tracked_file_hash[file_path] = 'file'

    return tracked_file_hash

def is_still_tracked(file_path, repo_root_path):
    try:
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", file_path],
            cwd=repo_root_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        # The file is no longer tracked
        return False

def process_gitignore(repo_root_path, gitignore_path, git_file_hash):
    with open(gitignore_path, 'r') as gitignore:
        lines_processed = 0
        for gitignore_entry in gitignore:
            gitignore_entry = gitignore_entry.strip()

            if gitignore_entry in git_file_hash and not gitignore_entry.startswith('#'):
                entry_type = git_file_hash[gitignore_entry]

                # Check if the file/dir is still tracked
                if is_still_tracked(gitignore_entry, repo_root_path):
                    # If still tracked, then proceed to untrack
                    if entry_type == 'directory':
                        command = ["git", "rm", "--cached", "-r", gitignore_entry]
                    else:
                        command = ["git", "rm", "--cached", gitignore_entry]

                    try: 
                        subprocess.run(command, 
                           cwd=repo_root_path,
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL, 
                           check=True)
                        print(f"The {entry_type} '{gitignore_entry}' has been successfully removed from tracking.")
                        lines_processed += 1
                    
                    except subprocess.CalledProcessError as e:
                        print(f"An error occurred while removing the {entry_type} {gitignore_entry} from tracking.")
                        print(e)
                else:
                    print(f"The {entry_type} '{gitignore_entry}' is already untracked.")

        if lines_processed == 0:
            print("No files in .gitignore were tracked, have a nice day!")
        else:
            print(f"{lines_processed} entries have been cleared")

def main():
    parser = argparse.ArgumentParser(description='Automatically untracks files and directories listed in a .gitignore file from a Git repository. '
                                                 'Operates on the specified path or defaults to the current directory.')

    parser.add_argument('-p','--path', help='Path to the directory or the .gitignore file (defaults to current directory)', default=os.getcwd())
    
    args = parser.parse_args()

    input_path = args.path

    # If input path is a directory add .gitignore
    if os.path.isdir(input_path):
        gitignore_path = os.path.join(input_path, '.gitignore')

    # Ensure file is a .gitignore 
    elif os.path.isfile(input_path) and input_path.endswith('.gitignore'):
        gitignore_path = input_path

    else:
        parser.error("ABORTING: The file provided is not a .gitignore")

    # Run the functions
    if os.path.exists(gitignore_path):
        tracked_files = get_tracked_files(input_path)
        process_gitignore(input_path, gitignore_path, tracked_files)
    else:
        parser.error("ERROR: .gitignore file not found. Make sure one exists...")

if __name__ == "__main__":
    main()