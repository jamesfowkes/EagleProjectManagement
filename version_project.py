#!/usr/bin/python3

import argparse
import os
import shutil
import time
import sys

from description import VersionDescription

def get_arg_parser():
    """ Return a command line argument parser for this module """
    arg_parser = argparse.ArgumentParser(
        description='Eagle Project Creation Script')

    arg_parser.add_argument(
        'name', metavar='N', type=str, nargs=1, help="Name of project to create")

    return arg_parser

def get_creation_date():
    return time.strftime("%d-%b-%y")
    
def get_creator_from_input():
    
    creator = input("Project Creator:")
    
    if creator == "":
        creator = "James Fowkes"
    
    return creator

def dirname_to_version(dirname):
    try:
        return float(dirname)
    except ValueError:
        return None
        
def get_highest_version(name):

    highest_version = 1.0
    
    for dir in os.listdir(name):
        version = dirname_to_version(dir)
        if version is not None:
            highest_version = max(version, highest_version)
            
    return highest_version
    
def up_project_version(name, increment=1.0):

    old_version = get_highest_version(name)
    new_version = old_version + increment
    
    print("Incrementing project '%s' version %.1f to %.1f" % (name, old_version, new_version))
               
    old_project_dir = "%s/%1.1f" % (name, old_version)
    new_project_dir = "%s/%1.1f" % (name, new_version)

    creator = get_creator_from_input()
    
    shutil.copytree(old_project_dir, new_project_dir)
    
    #Get the description from new project and write back
    desc = VersionDescription.from_project_version(name, new_version)
    desc.set_version(new_version)
    desc.write_description()

def main():
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    project_name = args.name[0] #Positional argument returned as array of one
    
    if not os.path.exists(project_name):
        sys.exit ("Project '%s' does not exist" % project_name)
    
    up_project_version(project_name)
    
if __name__ == "__main__":
    main()
