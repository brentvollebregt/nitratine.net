from flask import Flask, render_template, redirect

import data_managers



app = Flask(__name__, static_url_path='')
data = data_managers.JSON()



# API Routes

@app.route("/")
def homeRoute():
    return render_template('home.html')

@app.route("/projects")
def projectsRoute():
    return render_template('projects.html')

@app.route("/projects/<identifier>")
def projectsPageRoute(identifier):
    return ''

@app.route("/blog")
def blogRoute():
    return render_template('blog.html')

@app.route("/blog/<identifier>")
def blogPageRoute(identifier):
    return ''

@app.route("/youtube")
def youtubeRoute():
    return render_template('youtube.html')

@app.route("/youtube/<identifier>")
def youtubePageRoute(identifier):
    return ''

@app.route("/tools")
def toolsRoute():
    return render_template('tools.html')

@app.route("/tools/<identifier>")
def toolsPageRoute(identifier):
    return ''

@app.route("/aboutMe")
def aboutMeRoute():
    return render_template('aboutMe.html')



if __name__ == '__main__':
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    port = 8080
    print("Site starting on http://" + ip + ":" + str(port))
    app.run(debug=True, host=ip, port=port)