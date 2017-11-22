import json
import os
import time
import shutil

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
        }
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

    # Views

    def articleView(self, sub, article):
        self.data['articles'][sub][article]['views']['count'] += 1

        # TODO 7days in articles

        today = time.strftime('%d %b %y')
        if today in self.data['views']['daily']:
            self.data['views']['daily'][today] += 1
        else:
            self.data['views']['daily'][today] = 1

        hour = time.strftime('%H')
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

    # Getters

    @property
    def article_location(self):
        return self.data['articles_location']
