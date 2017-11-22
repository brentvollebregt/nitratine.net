from flask import Flask, render_template , url_for, render_template_string, send_from_directory, abort

import data_managers



app = Flask(__name__, static_url_path='')
data = data_managers.JSON()



# Routes

@app.route("/")
def homeRoute():
    top_articles = data.getArticlesByViews('home')
    recent_articles = data.getArticlesByDate('home', 5)
    return render_template('home.html', top_articles=top_articles, recent_articles=recent_articles)

@app.route("/projects")
def projectsRoute():
    return getSub('projects', "Projects")

@app.route("/projects/<article>")
def projectsPageRoute(article):
    return getArticle('projects', article)

@app.route("/blog")
def blogRoute():
    return getSub('blog', "Blog")

@app.route("/blog/<article>")
def blogPageRoute(article):
    return getArticle('blog', article)

@app.route("/apps")
def appsRoute():
    return getSub('apps', "Apps")

@app.route("/apps/<article>")
def appsPageRoute(article):
    return getArticle('apps', article)

@app.route("/youtube")
def youtubeRoute():
    return getSub('youtube', "YouTube")

@app.route("/youtube/<article>")
def youtubePageRoute(article):
    return getArticle('youtube', article)

@app.route("/tools")
def toolsRoute():
    return getSub('tools', "Tools")

@app.route("/tools/<article>")
def toolsPageRoute(article):
    return getArticle('tools', article)

@app.route("/stats") # TODO
def statsRoute():
    return render_template('stats.html')

@app.route("/non-static/<sub>/<article>/<img>")
def articleImageServing(sub, article, img):
    return send_from_directory(data.article_location + sub + "/" + article + "/", img)



# Recurring code

def getSub(sub, title):
    top_articles = data.getArticlesByViews(sub)
    recent_articles = data.getArticlesByDate(sub)
    return render_template('sub.html',
                           title=title,
                           display_icon=url_for('static', filename='img/' + sub + '-icon.svg'),
                           top_articles=top_articles,
                           recent_articles=recent_articles)

def getArticle(sub, article):
    if not data.articleExists(sub, article):
        abort(404)

    with open('articles/' + sub + '/' + article + '/view.html', 'r') as f:
        html = f.read()

    data.articleView(sub, article)
    return render_template_string(html, title=data.getArticleTitle(sub, article))



# For testing

@app.route("/json")
def jsonRoute():
    return str(data.data)



if __name__ == '__main__':
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    port = 8080
    print("Site starting on http://" + ip + ":" + str(port))
    app.run(debug=True, host=ip, port=port)
