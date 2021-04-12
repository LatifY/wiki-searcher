from flask import Flask, url_for, render_template, request, redirect, flash
import wikipedia
import os
import warnings

warnings.catch_warnings()
warnings.simplefilter("ignore")

#wikipedia.set_lang("tr")

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"

class Result:
    title:str
    summary:str

    def __init__(self, title, summary):
        self.title = title
        self.summary = summary

    def toDict(self):
        _dict = {"title":self.title, "summary":self.summary}
        return _dict

class Page:
    title:str
    content:str
    image:str

    def __init__(self,title,content, image= "https://via.placeholder.com/350x150"):
        self.title = title
        self.content = content
        self.image = image

    def toDict(self):
        _dict = {"title":self.title, "content":self.content, "image":self.image}
        return _dict

class Paragraph:
    header:str
    content:str

    def __init__(self,header="",content=""):
        self.header = header
        self.content = content

    def toDict(self):
        _dict = {"header":self.header, "content":self.content}

#Methods=======
def prefix(text, whatToChange, change_prefix):
    for change in whatToChange:
        text = text.replace(change, change_prefix)
    return text

def find_tags(text, _prefix):
    tag = False
    tags = []
    tagname = ""
    for i in range(len(text)):
        char = text[i]
        if char == _prefix:
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
    return tags
#Methods=======


@app.route("/", methods=["GET","POST"])
def home():
    if(request.method == "GET" and request.args.get("search") != None):
        search = request.args.get("search")
        print(search)
        search_results = wikipedia.search(search, results=5, suggestion=False)
        print(search_results)
        results = []
        for r in search_results:
            try:
                summary = wikipedia.summary(r, auto_suggest=False)
                if len(summary) > 200: summary = summary[:200]
                result = Result(r,summary)
                results.append(result.toDict())
            except:
                print(f"Couldnt find any result for {r}")

        return render_template('index.html', search=search,results=results)
    return render_template('index.html')

@app.route("/page/<query>")
def page(query):
    if "." in query:
        query = query.replace(".","")
    return redirect(url_for("info",query=query))
            
@app.route("/page/<query>/info")
def info(query):
    if "." in query:
        query = query.replace(".","")
    try:
        s = wikipedia.page(query)
        text = s.content
        text = text.replace(".\n",".\n\n")
        text = text.replace("?\n","?\n\n")
        text = text.replace("!\n","!\n\n")
        page = Page(s.title, text)
        return render_template("page.html", page=page.toDict())
    except wikipedia.exceptions.DisambiguationError as e:
        flash("Something went wrong!", "warning")
        return redirect(url_for("home"))

ignoreImages = ["https://upload.wikimedia.org/wikipedia/en/4/4a/Commons-logo.svg","https://upload.wikimedia.org/wikipedia/en/9/96/Symbol_category_class.svg",
"https://upload.wikimedia.org/wikipedia/en/d/db/Symbol_list_class.svg", "https://upload.wikimedia.org/wikipedia/en/8/8a/OOjs_UI_icon_edit-ltr-progressive.svg"
]
@app.route("/page/<query>/images")
def images(query):
    if "." in query:
        query = query.replace(".","")
    try:
        s = wikipedia.page(query)
        images = s.images
        for i in ignoreImages:
            if i in images:images.pop(images.index(i))
        for x in images:
            if images.count(x) > 1:
                for y in range(images.count(x) - 1):
                    images.pop(images.index(x))
        page = Page(s.title,"")
        return render_template("page.html", page=page.toDict() ,images=images)
    except:
        flash("Something went wrong!", "warning")
        return redirect(url_for("home"))

@app.errorhandler(404)
def page_not_found(error):
    return (render_template('404.html'), 404)
