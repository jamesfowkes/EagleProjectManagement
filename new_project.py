#!/usr/bin/python3

import argparse
import os
import shutil
import sys
from description import ProjectDescription, VersionDescription

def get_arg_parser():
    """ Return a command line argument parser for this module """
    arg_parser = argparse.ArgumentParser(
        description='Eagle Project Creation Script')

    arg_parser.add_argument(
        'name', metavar='N', type=str, nargs=1, help="Name of project to create")

    return arg_parser
   
def get_creator_from_input():
    return input("Project Creator:")
    
def get_description_from_input():
    
    first_line = ""
    while len(first_line) == 0:
        first_line = input("Project description Line 1 (must exist):")
        
    line_count = 2
    content = [first_line]
    finished = False
    
    while not finished:
        next_line = input("Project description Line %d (enter DONE to end):" % line_count)
        line_count += 1
        
        finished = next_line == "DONE"
        if not finished:
            content.append(next_line)
        else:
            break
            
    return content
    
def make_project(name):

    print("Creating project '%s'" % name)

    content = get_description_from_input()
    creator = get_creator_from_input()
    
    description = ProjectDescription(name, creator, content[0], content[1:])
    shutil.copytree("Project_Template", name)
    description.write_description()
 
    description = VersionDescription(name, creator, "1.0", ["???"], ["???"])
    description.write_description()
    
def main():
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    project_name = args.name[0] #Positional argument returned as array of one
    
    if os.path.exists(project_name):
        sys.exit ("Project '%s' already exists" % project_name)
    
    make_project(project_name)
    
if __name__ == "__main__":
    main()
