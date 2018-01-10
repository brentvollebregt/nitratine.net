from flask import Flask, render_template, url_for, render_template_string, send_from_directory, abort, session, request, redirect, jsonify, Response
import data_managers
import utils
import ast
import os
import json
import time
import importlib


app = Flask(__name__, static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 604800 # 1 Week
data = data_managers.JSON()
app.secret_key = data.secrty_key


# View Routes

@app.route("/")
def homeRoute():
    top_articles = data.getArticlesByViews('home', 8)
    recent_articles = data.getArticlesByDate('home', 8)
    return render_template('home.html',
                           top_articles=top_articles,
                           recent_articles=recent_articles,
                           extra_header_info=data.extra_header_info,
                           description=data.getStaticPageDescription('home'))

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

@app.route("/stats")
def statsRoute():
    total_views = data.getTotalViews()
    number_of_articles = data.getArticleCount()

    last_20_day_labels = data.getLast20DayLabels()
    last_20_day_data = data.getLast20DayData()
    prev_20_day_data = data.getPrev20DayData()

    hourly_data = data.getHourlyData()

    return render_template('stats.html',
                           total_views=str(total_views),
                           number_of_articles=str(number_of_articles),
                           last_20_day_labels=str(last_20_day_labels),
                           last_20_day_data=str(last_20_day_data),
                           prev_20_day_data=str(prev_20_day_data),
                           hourly_data=str(hourly_data),
                           time=time.strftime("%d %b %y, %H:%M:%S"),
                           description=data.getStaticPageDescription('stats'))

@app.route("/admin", methods=['GET', 'POST'])
def adminRoute():
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            redirects = data.redirects
            redirects_formatted = []
            for single_redirect in redirects:
                redirects_formatted.append(single_redirect + " -> " + redirects[single_redirect])
            return render_template('admin.html',
                                   redirects=redirects_formatted,
                                   descriptions=data.static_descriptions,
                                   ppv=data.pushPerView)
        else:
            return render_template('login.html')
    else:
        if request.json['username'] == data.username and request.json['password'] == data.password:
            session['logged_in'] = True
            return jsonify({'success' : True})
        return jsonify({'success' : False})

@app.route("/robots.txt")
def robotsRoute():
    return "Sitemap: " + data.site_location + "/sitemap.xml"

@app.route("/sitemap.xml")
def sitemapRoute():
    top = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    middle = ""

    middle += "  <url>\n    <loc>" + data.site_location + "</loc>\n    <priority>1.00</priority>\n  </url>\n"
    for sub in ['apps', 'blog', 'projects', 'tools', "youtube"]:
        middle += "  <url>\n    <loc>" + data.site_location + "/" + sub + "</loc>\n    <priority>0.80</priority>\n  </url>\n"
        for article in data.getArticleList(sub):
            middle += "  <url>\n    <loc>" + data.site_location + "/" + sub + "/" + article + "</loc>\n    <priority>0.64</priority>\n  </url>\n"

    bottom = "</urlset>"
    return top + middle + bottom

@app.errorhandler(404)
def page_not_found(e):
    if data.isARedirect(request.path):
        return redirect(data.getRedirect(request.path))
    return render_template('404.html'), 404


# Admin Routes

@app.route("/admin/push_json")
def adminPushJsonRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    data.writeFile()
    return jsonify({'success': True})

@app.route("/admin/rescrape")
def adminRescrapeRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    data.articleScrape()
    return jsonify({'success': True})

@app.route("/admin/article/download", methods=['POST'])
def adminDownloadArticleRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        filename = utils.zipArticle(data.article_location, request.form['sub'], request.form['article'])
        if filename:
            return send_from_directory(directory=utils.tmp_path, filename=filename, as_attachment=True, attachment_filename=filename)
        else:
            return jsonify({'success': False})
    except Exception as e:
        return jsonify({'success': False, 'reason' : str(e)})

@app.route("/admin/article/delete", methods=['POST'])
def adminDeleteArticleRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        sub = request.json['sub']
        url = request.json['url']
        utils.deleteArticleFiles(data.article_location, sub, url)
        data.removeArticle(sub, url)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'reason' : str(e)})

@app.route("/admin/article/upload", methods=['POST'])
def adminCreateArticleRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        sub = request.form['sub']
        url = request.form['article']
        file = request.files['file']
        file.save(os.getcwd() + '/zip.zip')
        utils.unzipArticle(data.article_location, sub, url)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'reason' : str(e)})

@app.route("/admin/json/download")
def adminDownloadJsonRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    return jsonify({'success': True, 'data' : data.data})

@app.route("/admin/json/upload", methods=['POST'])
def adminUploadJsonRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        if type(request.json['data']) == dict:
            data.data = request.json['data']
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'reason': "Not in JSON format"})
    except Exception as e:
        return jsonify({'success': False, 'reason': str(e)})

@app.route("/admin/redirects/add", methods=['POST'])
def adminRedirectsAddRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        data.addRedirect(request.json['from'], request.json['to'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': True, 'reason': str(e)})

@app.route("/admin/redirects/remove", methods=['POST'])
def adminRedirectsRemoveRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        data.removeRedirect(request.json['redirect'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': True, 'reason': str(e)})

@app.route("/admin/article_folder/upload", methods=['POST'])
def adminArticleFolderUploadRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        request.files['file'].save(os.getcwd() + '/zip.zip')
        utils.unzipArticleFolder(data.article_location)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': True, 'reason': str(e)})

@app.route("/admin/article_folder/download")
def adminArticleFolderDownloadRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        filename = utils.zipArticleFolder(data.article_location)
        if filename:
            return send_from_directory(directory=utils.tmp_path, filename=filename, as_attachment=True, attachment_filename=filename)
        else:
            return jsonify({'success': False})
    except Exception as e:
        return jsonify({'success': True, 'reason': str(e)})

@app.route("/admin/modify_description/<page>", methods=['POST'])
def adminModifyDescriptionRoute(page):
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        data.setStaticPageDescription(page, request.json['desc'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': True, 'reason': str(e)})

@app.route("/admin/set_site_location")
def adminSetSiteLocationRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        data.setSiteLocation(request.url_root[:-1])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': True, 'reason': str(e)})

@app.route("/admin/add_me_to_ip_blacklist")
def adminAddMeToIPBlacklistRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        data.addIPViewBlacklisted(request.remote_addr)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': True, 'reason': str(e)})

@app.route("/admin/set_push_per_view", methods=['POST'])
def adminSetPushPerViewRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    try:
        data.setPushPerView(request.json['enable'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': True, 'reason': str(e)})

@app.route("/admin/download_stats")
def adminDownloadStatsRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    return Response(json.dumps(data.getDownloadableStats()),
                    mimetype='application/json',
                    headers={'Content-Disposition': 'attachment;filename=stats.json'})

@app.route("/admin/logout")
def adminLogoutRoute():
    session['logged_in'] = False
    return redirect(url_for('adminRoute'))


# Work Routes

@app.route("/non-static/<sub>/<article>/<img>")
def articleImageServing(sub, article, img):
    return send_from_directory(data.article_location + sub + "/" + article + "/", img)

@app.route("/script/<sub>/<article>/<script>", methods=['POST'])
def articleScriptServing(sub, article, script):
    module_string = "articles." + sub + '.' + article + '.' + script
    module = importlib.import_module(module_string)
    return module.main(request)


# Recurring code

def getSub(sub, title):
    top_articles = data.getArticlesByViews(sub)
    recent_articles = data.getArticlesByDate(sub)
    return render_template('sub.html',
                           title=title,
                           display_icon=url_for('static', filename='img/' + sub + '-icon.svg'),
                           top_articles=top_articles,
                           recent_articles=recent_articles,
                           extra_header_info=data.extra_header_info,
                           description=data.getStaticPageDescription(sub))

def getArticle(sub, article):
    if not data.articleExists(sub, article):
        abort(404)

    with open(data.article_location + sub + '/' + article + '/view.html', 'r') as f:
        html = f.read()

    data.articleView(sub, article, request.remote_addr)
    return render_template_string(html,
                                  title=data.getArticleTitle(sub, article),
                                  date=data.getArticleDate(sub, article),
                                  views=data.getArticleViews(sub, article),
                                  description=data.getArticleDescription(sub, article),
                                  extra_header_info=data.extra_header_info,
                                  relative_url='/' + sub + '/' + article)

def convertDateToReadable(timestamp):
    return time.strftime('%d %b %y', time.localtime( int(timestamp) ))


app.jinja_env.globals.update(convertDateToReadable=convertDateToReadable)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    port = 8080
    print("Site starting on http://" + ip + ":" + str(port))
    app.run(host=ip, port=port)
