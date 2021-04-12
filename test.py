import wikipedia
import warnings
import re
import time
from datetime import datetime
prefix = "|"

class Paragraph:
    title:str
    content:str

    def __init__(self,title,content):
        self.title = title
        self.content = content

    def toDict(self):
        _dict = {"title":self.title, "content":self.content}

p = wikipedia.page("Jazz")
text = p.content

text = text.replace("=====", prefix)
text = text.replace("====", prefix)
text = text.replace("===", prefix)
text = text.replace("==", prefix)

tag = False
tags = []
tagname = ""
for i in range(len(text)):
    char = text[i]
    if char == prefix:
        if tag == False:
            tag = True
        else:
            if tagname != "": tags.append(tagname.strip())
            tagname = ""
            tag = False
    else:
        if tag == True:
            if char != "" and char != "\n":
                tagname += char
