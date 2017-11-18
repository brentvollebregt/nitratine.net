import json
import os
import time

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
            "today" : {
                "count" : 0,
                "date" : 1483182000
            },
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
                        "title" : article_data["title"],
                        "title_reduced" : article_data["title_reduced"],
                        "description" : article_data["description"],
                        "tags" : article_data["tags"],
                        "date" : time.mktime( time.strptime(article_data["date"], "%d %b %y") ),
                        "views" : {
                            "count" : 0,
                            "30days" : {}
                        }
                    }

    # Views

    def viewDayRollOverCheck(self):
        pass

    def articleView(self, sub, article):
        self.data['articles'][sub][article]['views']['count'] += 1

        # TODO Daily in article

        # TODO Global today (check date to see if needs to be rotated)

        hour = time.strftime('%H')
        if hour not in self.data['views']['hours']:
            self.data['views']['hours'][hour] = 1
        else:
            self.data['views']['hours'][hour] += 1

        self.data['views']['count'] += 1

    # Getters

    @property
    def article_location(self):
        return self.data['articles_location']
