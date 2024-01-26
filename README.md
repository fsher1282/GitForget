# GitForget

## Overview
`GitForget` is a Python script designed to address a common scenario in version control workflows: when `.gitignore` is updated after files have already been tracked by Git. In such cases, simply updating `.gitignore` doesn't automatically untrack the previously tracked files. `GitForget` automates the process of untracking these files, aligning your repository's tracked files with the current `.gitignore` rules.

## Features
- Untracks files and directories that are listed in `.gitignore` but were previously tracked by Git.
- Can operate on specified directories or default to the current directory if no path is provided.
- Provides clear, user-friendly feedback about the changes being made.
- Offers a safe way to ensure `.gitignore` updates are effectively reflected in the repository.

## Prerequisites
Before running `GitForget`, ensure you have the following:
- Python 3.x installed on your system.
- A Git repository where you have sufficient permissions to modify file tracking.

## Usage

To use `GitForget`, follow these steps:

1. Clone or download the `GitForget` script to your local system.
2. Navigate to the root of your Git repository in your command line or terminal.
3. Run the script using Python:

   ```bash
   python3 GitForget.py [-p /path/to/repository]
