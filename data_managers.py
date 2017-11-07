import json

class JSON():

    file_location = "data.json"
    default_data = {}

    def __init__(self):
        self.getFile()
        if self.data is None:
            self.createDefaultFile()

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
