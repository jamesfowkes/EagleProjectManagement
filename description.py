#!/usr/bin/python3

import time
import re

from html.parser import HTMLParser

class Description:

    class ProjectParser(HTMLParser):
    
        def __init__(self):
            self.tags = []
            self.lines = []
            super().__init__()
            
        def handle_starttag(self, tag, attrs):
            self.tags.append((tag, attrs))
        
        def handle_startendtag(self, tag, attrs):
            self.lines.append("")
            
        def handle_endtag(self, tag):
            self.tags.pop()
    
        def handle_data(self, data):
            
            try:
                (tag, attrs) = self.tags[-1]
            
                if tag == "b" and attrs[0][0] == "id" and attrs[0][1] == "title":
                    self.title = data
                    
                elif tag == "creator":
                    self.creator = data
                
                elif tag == "date":
                    self.date = data
                    
                elif tag == "span" and attrs[0][1] == "desc":
                    self.lines.append(data)
            except:
                pass
                    
    class VersionParser(HTMLParser):
        
        def __init__(self):
            self.tags = []
            self.todo = []
            self.done = []
            super().__init__()
            
        def handle_starttag(self, tag, attrs):
            self.tags.append((tag,attrs))
            
        def handle_endtag(self, tag):
            self.tags.pop()
            
        def handle_data(self, data):
            
            try:
                (tag, attrs) = self.tags[-1]
            except IndexError:
                (tag, attrs) = (None, None)

            if tag == "ver":
                self.version = data
                
            if tag == "creator":
                self.creator = data
            
            if tag == "date":
                self.date = data
    
            if tag == "ul":
                self.list_type = attrs[0][1]
                
            if tag == "li":
                if self.list_type == "todo":
                    self.todo.append(data)
                    
                if self.list_type == "done":
                    self.done.append(data)
      
    def __init__(self, project_name, creator, create_date=None):
        
        self.project_name = project_name
        
        if creator is None:
            self.creator = "James Fowkes"
        else:
            self.creator = creator
        
        if create_date is None:
            self.create_date = time.strftime("%d-%b-%y")
        else:
            self.create_date = create_date
    
    def __repr__(self):
        return "Description('%r', '%r', '%r', '%r')" % (self.project_name, self.content_lines, self.creator, self.create_date)
        
    @staticmethod
    def __getCreator(line):
        result = re.search('<creator>(.*)</creator>', line)
        return result.group(1)
    
    @staticmethod
    def __getDate(line):
        result = re.search('<date>(.*)</date>', line)
        return result.group(1)
       
    def _get_creation_line(self):
        return self.get_creation_line(self.creator, self.create_date)
                  
    @staticmethod
    def get_creation_line(creator, date):
        return "Created by <creator>%s</creator> on <date>%s</date>" % (creator, date)
        
    def write_description(self, stream=None):

        #Assume we want to write to project description file, otherwise to the provided stream
        if stream is None:
            with open(self._path(), 'w') as f:
                f.write(self.to_html())
        else:
            stream.write(self.to_html())
            
class ProjectDescription(Description):
    def __init__(self, project_name, creator, title, content, create_date=None):
        super().__init__(project_name, creator, create_date)
        self.title = title
        self.content = content

    @classmethod
    def from_project(cls, project):
        with open(cls.description_path_for_project(project), 'r') as f:
            return cls.from_html(project, f.readlines())
            
    @classmethod
    def from_html(cls, project, html):
        
        parser = cls.ProjectParser()
        parser.feed(html)
        
        return cls(project, parser.creator, parser.title, parser.lines, parser.date)
        
    def to_html(self):
        description_html = """
        <p>
            <b id='title'>%s</b>
            <br/>
            <br/>
            %s
            <br/>
            %s
            </p>""" % (self.title, self.content_to_spans(self.content), self._get_creation_line())

        return description_html
    
    def _path(self):
        return "%s/DESCRIPTION" % self.project_name
            
    @staticmethod
    def content_to_spans(content):
        spans = []
        for line in content:
            if line == "":
                spans.append("<br/>")
            else:
                spans.append("<span id='desc'>%s</span><br/>" % line)
                
        return "\n".join(spans)
    
class VersionDescription(Description):
    def __init__(self, project_name, creator, version, todo, done, create_date=None):
        super().__init__(project_name, creator, create_date)
        self.version = version
        self.todo = todo
        self.done = done
    
    def set_version(self, new_version):
        self.version = new_version
        
    @classmethod
    def from_project_version(cls, project, version):
        with open(cls._version_path(project, version), 'r') as f:
            return cls.from_html(project, f.read())
            
    @classmethod
    def from_html(cls, project, html):
        
        parser = cls.VersionParser()
        
        parser.feed(html)   
        
        return cls(project, parser.creator, parser.version, parser.todo, parser.done, parser.date)
    
    @staticmethod
    def __to_list(items, list_id):
        items = '\n'.join(["<li>%s</li>" % item for item in items])
        
        return """
        %s
        <ul id='%s'>
        
        %s
        </ul>
        """ % (list_id, list_id.lower(), items)
        
    def to_html(self):
        description_html = """
            <p>
                <b>Version <ver>%s</ver></b>
                <br/>
                <br/>
                %s
                %s
                <br/>
                %s
            </p>""" % (self.version, self.__to_list(self.todo, "ToDo"), self.__to_list(self.done, "Done"), self._get_creation_line())
            
        return description_html
    
    @staticmethod 
    def _version_path(name, version):
        return "%s/%s/DESCRIPTION" % (name, version)
        
    def _path(self):
        return self._version_path(self.project_name, self.version)

if __name__ == "__main__":

    # Do some basic testing of the Description class
    
    #######################################
    
    in_html = """
    <p>
        <b id='title'>A sample description</b>
        <br/>
        <span id='desc'>With some linebreaks</span>
        <br/>
        <span id='desc'>between</span>
        <br/>
        <span id='desc'>lines</span>
        <br/>
        %s
    </p>
    """ % Description.get_creation_line("JamesF", "08-Aug-14")
    
    desc = ProjectDescription.from_html("Project Name", in_html)
    out_html = desc.to_html()
    
    ## Uncomment to test HTML-to-HTML project description
    #print("In:")
    #print(in_html)

    #print("Out:")
    #print(out_html)

    #######################################
    
    desc = ProjectDescription("Project Name", "JamesF", "Line1", ["Line2", "", "Line3"])
    out_html = desc.to_html()
    
    ## Uncomment to test constructor-to-HTML project description
    #print("Out:")
    #print(out_html)
    
    #######################################
    
    in_html = """
    <p>
        <b>Version <ver>1.0</ver></b>
        <p>Todo:
        <ul id="todo">
            <li>Todo1</li>
            <li>Todo2</li>
        </ul>
        </p>
        <p>Done
        <ul id="done">
            <li>Done1</li>
            <li>Done2</li>
        </ul>
        </p>
        %s
    </p>
    """ % Description.get_creation_line("JamesF", "08-Aug-14")
    
    desc = VersionDescription.from_html("Project Name", in_html)
    out_html = desc.to_html()

    #Uncomment to test HTML-to-HTML version description
    #print("In:")
    #print(in_html)

    #print("Out:")
    #print(out_html)
    
    #######################################
    
    desc = VersionDescription("Project Name", "James Fowkes", "1.0", ["Todo1", "Todo2"], ["Done1", "Done2"])
    out_html = desc.to_html()
    
    ## Uncomment to test constructor-to-HTML version description
    print("Out:")
    print(out_html)
