import json
import os
import time
import shutil
import string
import random

class JSON():

    file_location = "data.json"
    default_data = {
        "articles" : {
            "apps" : {},
            "blog" : {},
            "projects" : {},
            "tools" : {},
            "youtube" : {}
        },
        "views" : {
            "daily" : {},
            "hours" : {},
            "count" : 0
        },
        "administration" : {
            "username" : "",
            "password" : ""
        },
        "descriptions" : {
            "home" : "Nitratine is the home of my projects, tutorials and tools. I built the backend myself using Python and Flask.",
            "apps" : "This is a showcase of the apps that I have made and the background of how and why they came about.",
            "blog" : "This is where most of my experiments are recorded as sometimes I need to experiment concepts for some projects.",
            "projects" : "These are the projects I have made and contributed to. I show how they work and how to install and use them.",
            "tools" : "These are small tools that I always need around but can't find or they function too bad.",
            "youtube" : "These articles are written tutorials of the YouTube channel PyTutorials. This also contains quick fixes for things that people have found coming up.",
            "stats" : "Statistics including total views and articles, when people visited and where in the day."
        },
        "secrty_key" : "secret",
        "site_location" : "",
        "redirects" : {},
        "redirects_request_count" : {},
        "push_per_view" : 1,
        "view_ip_blacklist" : [],
        "enable_right_sidebar" : True,
        "external" : {
            "google-site-verification" : "",
            "google-analytics" : "",
            "ads" : {
                "enabled" : True,
                "300x250_code" : ""
            },
            "youtube_channel_id" : "",
            "youtube_data_API_key" : ""
        }
    }

    def __init__(self):
        self.getFile()
        if self.data is None:
            self.createDefaultFile()
        self.checkDirStructure()
        self.articleScrape()

    # File writing

    def getFile(self):
        try:
            with open(self.file_location, 'r') as data_file:
                self.data = json.load(data_file)
        except:
            self.data = None

    def writeFile(self):
        with open(self.file_location, 'w') as outfile:
            json.dump(self.data, outfile)

    def createDefaultFile(self):
        self.data = self.default_data
        self.writeFile()

    def checkDirStructure(self):
        for sub in ['apps', 'blog', 'projects', 'tools', 'youtube']:
            if not os.path.exists(self.article_location + sub):
                os.makedirs(self.article_location + sub)

    def createBackup(self):
        self.writeFile()

        save_location = 'backups/'
        max_backup_files = 5

        if not os.path.exists(save_location):
            os.makedirs(save_location)

        save_as = save_location + time.strftime("%d-%b-%y_%H-%M-%S") + '_data.json'
        shutil.copy('data.json', save_as)

        if len(os.listdir(save_location)) > max_backup_files:
            files = {}
            for file in os.listdir(save_location):
                files[os.path.getmtime(save_location + file)] = file

            oldest = files[sorted(files)[0]]
            os.remove(save_location + oldest)

    # Articles

    def articleScrape(self):
        subs = ['apps', 'blog', 'projects', 'tools', 'youtube']
        for sub in subs:
            for article in os.listdir(self.article_location + sub):
                try:
                    with open(self.article_location + sub + "/" + article + "/data.json", 'r') as article_json_file:
                        article_data = json.load(article_json_file)
                    if article not in self.data['articles'][sub]:
                        self.data['articles'][sub][article] = {
                            "sub" : sub,
                            "url_ext" : article,
                            "views" : {
                                "count" : 0,
                                "7days" : {}
                            }
                        }
                    self.data['articles'][sub][article]['title'] = article_data["title"]
                    self.data['articles'][sub][article]['description'] = article_data["description"]
                    self.data['articles'][sub][article]['date'] = time.mktime( time.strptime(article_data["date"], "%d %b %y") )
                except Exception as e:
                    self.data['articles'][sub][article]['error'] = True
                    self.data['articles'][sub][article]['reason'] = str(e)
                    self.data['articles'][sub][article]['day'] = time.strftime("%d %b %y, %H:%M:%S")

    def articleExists(self, sub, article):
        if article in self.data['articles'][sub]:
            return True
        else:
            return False

    def getArticleTitle(self, sub, article):
        return self.data['articles'][sub][article]['title']

    def getArticleDate(self, sub, article):
        return time.strftime("%d %b %y", time.localtime(int(self.data['articles'][sub][article]['date'])))

    def getArticleViews(self, sub, article):
        return self.data['articles'][sub][article]['views']['count']

    def getArticleDescription(self, sub, article):
        return self.data['articles'][sub][article]['description']

    def removeArticle(self, sub, article):
        if sub in self.data['articles'] and article in self.data['articles'][sub]:
            del self.data['articles'][sub][article]

    def getArticleList(self, sub):
        return [article for article in self.data['articles'][sub]]

    def moveArticle(self, sub, article, new_sub):
        self.data['articles'][new_sub][article] = self.data['articles'][sub][article]
        del self.data['articles'][sub][article]

    # Redirects

    def isARedirect(self, path):
        return path in self.data['redirects']

    def getRedirect(self, path):
        self.data['redirects_request_count'][path] += 1
        return self.data['redirects'][path]

    def getRedirectCount(self, path):
        return self.data['redirects_request_count'][path]

    def addRedirect(self, path, to):
        self.data['redirects'][path] = to
        self.data['redirects_request_count'][path] = 0

    def removeRedirect(self, path):
        if path in self.data['redirects']:
            del self.data['redirects'][path]
            del self.data['redirects_request_count'][path]

    # Views

    def articleView(self, sub, article, ip):
        if self.isIPViewBlacklisted(ip):
            return

        today = time.strftime('%d %b %y')
        hour = time.strftime('%H')

        self.data['articles'][sub][article]['views']['count'] += 1

        if today in self.data['articles'][sub][article]['views']['7days']:
            self.data['articles'][sub][article]['views']['7days'][today] += 1
        else:
            self.data['articles'][sub][article]['views']['7days'][today] = 1
        if len(self.data['articles'][sub][article]['views']['7days']) > 7:
            dates = [i for i in self.data['articles'][sub][article]['views']['7days']]
            dates_formatted = [time.strptime(date, '%d %b %y') for date in dates]
            ealiest_entry = time.strftime('%d %b %y', min(dates_formatted) )
            del self.data['articles'][sub][article]['views']['7days'][ealiest_entry]

        if today in self.data['views']['daily']:
            self.data['views']['daily'][today] += 1
        else:
            self.data['views']['daily'][today] = 1

        if hour not in self.data['views']['hours']:
            self.data['views']['hours'][hour] = 1
        else:
            self.data['views']['hours'][hour] += 1

        self.data['views']['count'] += 1

        if self.pushPerView:
            self.writeFile()

    # View IP Blacklist

    def isIPViewBlacklisted(self, ip):
        return ip in self.data['view_ip_blacklist']

    def addIPViewBlacklisted(self, ip):
        if ip not in self.data['view_ip_blacklist']:
            self.data['view_ip_blacklist'].append(ip)

    # Article Display

    def getArticlesInSub(self, sub):
        if sub == "home":
            subs = ['apps', 'blog', 'projects', 'tools', 'youtube']
        else:
            subs = [sub]

        articles = []
        for sub in subs:
            for article in self.data['articles'][sub]:
                articles.append(self.data['articles'][sub][article])

        return articles

    def getArticlesByViews(self, sub, limit=5):
        articles = self.getArticlesInSub(sub)
        sorted_articles = sorted(articles, key=lambda x: x['views']['count'], reverse=True)

        return sorted_articles[:limit]

    def getArticlesByDate(self, sub, limit=False):
        articles = self.getArticlesInSub(sub)
        sorted_articles = sorted(articles, key=lambda x: x['date'], reverse=True)

        if limit:
            return sorted_articles[:limit]
        return sorted_articles

    # Statistics

    def getTotalViews(self):
        return self.data['views']['count']

    def getArticleCount(self):
        return len([article for sub in self.data['articles'] for article in self.data['articles'][sub]])

    def getLast20DayLabels(self):
        labels_datefmt = [time.strptime(date, "%d %b %y") for date in self.data['views']['daily']]
        labels_datefmt.sort()
        labels = [time.strftime("%d %b %y", label) for label in labels_datefmt]
        return labels[-20:]

    def getLast20DayData(self):
        return [self.data['views']['daily'][label] for label in self.getLast20DayLabels()]

    def getPrev20DayData(self):
        days_recorded = [date for date in self.data['views']['daily']]
        for date in self.getLast20DayLabels():
            days_recorded.remove(date)
        labels_datefmt = [time.strptime(date, "%d %b %y") for date in days_recorded]
        labels_datefmt.sort()
        labels = [time.strftime("%d %b %y", label) for label in labels_datefmt]
        return [self.data['views']['daily'][label] for label in labels[-20:]]

    def getHourlyData(self):
        hourly_data = []
        for hour in range(24):
            hour = str(hour).zfill(2)
            if hour in self.data['views']['hours']:
                data = self.data['views']['hours'][hour]
            else:
                data = 0
            hourly_data.append(data)
        return hourly_data

    def getDownloadableStats(self):
        stats = {'views' : self.data['views'], 'articles' : {}}
        for sub in self.data['articles']:
            stats['articles'][sub] = {}
            for article in self.data['articles'][sub]:
                stats['articles'][sub][article] = self.data['articles'][sub][article]['views']
        return stats

    # Static Location Descriptions

    def getStaticPageDescription(self, sub):
        return self.data['descriptions'][sub]

    def setStaticPageDescription(self, page, desc):
        self.data['descriptions'][page] = desc

    # External

    def getRightSidebarAd(self):
        if self.data['external']['ads']['enabled']:
            return self.data['external']['ads']['300x250_code']
        return ''

    @property
    def youtube_channel_id(self):
        return self.data['external']['youtube_channel_id']

    @property
    def youtube_data_API_key(self):
        return self.data['external']['youtube_data_API_key']

    @property
    def google_site_verification(self):
        return self.data['external']['google-site-verification']

    @property
    def google_analytics(self):
        return self.data['external']['google-analytics']

    # Right sidebar

    def setRightSidebarEnabled(self, enabled):
        self.data['enable_right_sidebar'] = enabled

    @property
    def enable_right_sidebar(self):
        return self.data['enable_right_sidebar']

    # Other Site Settings

    def setSiteLocation(self, location):
        self.data['site_location'] = location

    def setPushPerView(self, ppv):
        self.data['push_per_view'] = ppv

    # Getters

    @property
    def article_location(self):
        return os.path.dirname(os.path.realpath(__file__)) + '/articles/'

    @property
    def secrty_key(self):
        if 'secrty_key' in self.data:
            return self.data['secrty_key']
        else:
            print ("WARN: Generating own secret key")
            self.data['secrty_key'] = ''.join([random.choice(string.punctuation + string.digits + string.ascii_letters) for i in range(32)])
            return self.data['secrty_key']

    @property
    def username(self):
        return self.data['administration']['username']

    @property
    def password(self):
        return self.data['administration']['password']

    @property
    def site_location(self):
        return self.data['site_location']

    @property
    def static_descriptions(self):
        return self.data['descriptions']

    @property
    def redirects(self):
        return self.data['redirects']

    @property
    def pushPerView(self):
        return self.data['push_per_view']
