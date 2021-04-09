from flask import Flask, url_for, render_template, request, redirect, flash
import wikipedia
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"

class Result:
    title:str
    content="deneme"
    summary:str
    def __init__(self, title, summary):
        self.title = title
        self.summary = summary

    def editContent(self,content):
        self.content = content

    def toArray(self):
        lst = [self.title,self.content,self.summary]
        return lst

@app.route("/", methods=["GET","POST"])
@app.route("/search", methods=["GET","POST"])
def home():
    if(request.method == "POST"):
        search = request.form["search"]
        can_suggestion = request.form.get("can_suggestion")
        search_results = wikipedia.search(search, results=5, suggestion=True)
        suggestion = search_results[1]
        if(suggestion != None and can_suggestion and search_results[0] == None):
            search = suggestion
            search_results = wikipedia.search(search,results = 5, suggestion=True)
        print(search_results)
        results = []
        for r in search_results[0]:
            try:
                summary = wikipedia.summary(r, auto_suggest=False)
                if len(summary) > 200: summary = summary[:200]
                result = Result(r,summary)
                results.append(result.toArray())
            except:
                print(f"Couldnt find any result for {r}")
        return render_template('index.html', search=search,results=results, can_suggestion = can_suggestion)
    flash("Makale bulunamadı","warning")
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return (render_template('404.html'), 404)
