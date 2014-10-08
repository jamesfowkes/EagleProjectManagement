#!/bin/python3

import time
import re

class Description:

    def __init__(self, project_name, content_lines, creator, create_date=None):
        
        self.project_name = project_name
        if creator is None:
            self.creator = "James Fowkes"
        else:
            self.creator = creator
        
        if create_date is None:
            self.create_date = time.strftime("%d-%b-%y")
        else:
            self.create_date = create_date
            
        self.content_lines = content_lines
       
    @property
    def __root_path(self):
        return self.description_path_for_project(self.project_name)
    
    @property
    def __version_path(self, version):
        return self.description_path_for_project_version(self.project_name, version)
        
    def write_description_to_project(self, stream=None):

        #Assume we want to write to project description file, otherwise to the provided stream
        if stream is None:
            with open(self.__root_path, 'w') as f:
                f.write(self.html())
        else:
            stream.write(self.html())
    
    @staticmethod
    def __getCreator(line):
        result = re.search('<creator>(.*)</creator>', line)
        return result.group(1)
    
    @staticmethod
    def __getDate(line):
        result = re.search('<date>(.*)</date>', line)
        return result.group(1)

    @classmethod
    def from_html(cls, project, html):
    
        content = []
        count = 0
        for line in html:
            count += 1
            line_has_creator = "<creator>" in line
            line_has_date = "<date>" in line
            
            if line_has_creator or line_has_date:
                if line_has_creator:
                    creator = cls.__getCreator(line)
                if line_has_date:
                    date = cls.__getDate(line)
            else:
                content.append(line)
        
        print(content)
        
        return cls(project, content_lines, creator, date)
    
    @classmethod
    def from_project(cls, project):
        with open(self.description_path, 'r') as f:
            return load_from_html(f.readlines())
            
        
    def html(self):

        description_html = """
        <p>
            <b>%s</b>
            %s
            <br>
            <br>
            %s
        </p>""" % (self.content_lines[0], ''.join(self.content_lines[1:]), self.__get_creation_line())
            
        return description_html
    
    def __get_creation_line(self):
        return self.get_creation_line(self.creator, self.create_date)
        
    @staticmethod
    def description_path_for_project(name):
        return "%s/DESCRIPTION" % name
    
    @staticmethod
    def description_path_for_project_version(name, version):
        return "%s/%s/DESCRIPTION" % (name, version)

    @staticmethod
    def get_creation_line(creator, date):
        return "Created by <creator>%s</creator> on <date>%s</date>" % (creator, date)
        
if __name__ == "__main__":

    # Do some basic testing of the Description class
    
    desc_html = """
    <p>A sample description<br>
    With some linebreaks<br></p>
    %s""" % Description.get_creation_line("JamesF", "08-Aug-14")
    
    desc = Description.from_html("Project Name", desc_html.split('\n'))
    
    print(desc.project_name)
    print(desc.content)
    print(desc.creator)
    print(desc.create_date)
    
    print(desc.html())
    