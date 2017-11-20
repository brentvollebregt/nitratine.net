from flask import Flask, render_template, redirect, url_for, render_template_string, send_from_directory

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
    return render_template('sub.html',
                           title="Projects",
                           display_icon=url_for('static', filename='img/project-icon.svg')
                           )

@app.route("/projects/<article>")
def projectsPageRoute(article):
    return ''

@app.route("/blog")
def blogRoute():
    return render_template('sub.html',
                           title="Blog",
                           display_icon=url_for('static', filename='img/blog-icon.svg')
                           )

@app.route("/blog/<article>")
def blogPageRoute(article):
    return ''

@app.route("/apps")
def appsRoute():
    return render_template('sub.html',
                           title="Apps",
                           display_icon=url_for('static', filename='img/apps-icon.svg')
                           )

@app.route("/apps/<article>")
def appsPageRoute(article):
    # TODO Check if article exists in JSON
    with open('articles/apps/' + article + '/view.html', 'r') as f:
        html = f.read()

    data.articleView('apps', article)
    return render_template_string(html, title="Apps")

@app.route("/apps/<article>/bug-report")
def appsBugRoute(article):
    return ''

@app.route("/youtube")
def youtubeRoute():
    return render_template('sub.html',
                           title="YouTube",
                           display_icon=url_for('static', filename='img/youtube-icon.svg')
                           )

@app.route("/youtube/<article>")
def youtubePageRoute(article):
    return ''

@app.route("/tools")
def toolsRoute():
    return render_template('sub.html',
                           title="Tools",
                           display_icon=url_for('static', filename='img/tools-icon.svg')
                           )

@app.route("/tools/<article>")
def toolsPageRoute(article):
    return ''

@app.route("/stats")
def statsRoute():
    return render_template('stats.html')

@app.route("/non-static/<sub>/<article>/<img>")
def articleImageServing(sub, article, img):
    return send_from_directory(data.article_location + sub + "/" + article + "/", img)



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
