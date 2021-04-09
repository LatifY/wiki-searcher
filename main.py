from flask import Flask, url_for, render_template, request, redirect, flash
import wikipedia
import os

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
    try:
        s = wikipedia.page(query)
        print("arama")
        page = Page(s.title, s.content)
        print("sayfa")
    except:
        flash("Something went wrong!", "warning")
        return redirect(url_for("home"))
    return render_template("page.html", page=page.toDict())

@app.errorhandler(404)
def page_not_found(error):
    return (render_template('404.html'), 404)
