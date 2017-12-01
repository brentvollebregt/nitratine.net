import json
import os
import time
import shutil
import string
import random

class JSON():

    file_location = "data.json"
    default_data = {
        "articles_location" : "articles/",
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
        "secrty_key" : "secret"
    }

    def __init__(self):
        self.getFile()
        if self.data is None:
            self.createDefaultFile()
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
            json.dump(self.data, outfile) # , indent=4, sort_keys=True (without saves computation)

    def createDefaultFile(self):
        self.data = self.default_data
        self.writeFile()

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
                if article not in self.data['articles'][sub]:
                    with open(self.article_location + sub + "/" + article + "/data.json", 'r') as article_json_file:
                        article_data = json.load(article_json_file)
                    self.data['articles'][sub][article] = {
                        "sub" : sub,
                        "url_ext" : article,
                        "title" : article_data["title"],
                        "title_reduced" : article_data["title_reduced"],
                        "description" : article_data["description"],
                        "tags" : article_data["tags"],
                        "date" : time.mktime( time.strptime(article_data["date"], "%d %b %y") ),
                        "views" : {
                            "count" : 0,
                            "7days" : {}
                        }
                    }

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

    # Views

    def articleView(self, sub, article):
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

    def getArticlesByViews(self, sub):
        articles = self.getArticlesInSub(sub)
        sorted_articles = sorted(articles, key=lambda x: x['views']['count'], reverse=True)

        return sorted_articles[:5]

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

    # Getters

    @property
    def article_location(self):
        return self.data['articles_location']

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
