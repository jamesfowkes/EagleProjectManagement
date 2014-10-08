#!/bin/python3

import argparse
import os
import shutil
import sys
from description import Description

def get_arg_parser():
    """ Return a command line argument parser for this module """
    arg_parser = argparse.ArgumentParser(
        description='Eagle Project Creation Script')

    arg_parser.add_argument(
        'name', metavar='N', type=str, nargs=1, help="Name of project to create")

    return arg_parser
   
def get_creator_from_input():
    creator = input("Project Creator:")
    
def make_project(name):

    print("Creating project '%s'" % name)
           
    content = input("Project description (use <br> for line breaks):")
    creator = get_creator_from_input()
    
    description = Description(name, content, creator)
    shutil.copytree("Project_Template", name)
    description.write_description_to_project()
    
def main():
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    project_name = args.name[0] #Positional argument returned as array of one
    
    if os.path.exists(project_name):
        sys.exit ("Project '%s' already exists" % project_name)
    
    make_project(project_name)
    
if __name__ == "__main__":
    main()