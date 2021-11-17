import pyrebase


class Model:
    def __init__(self):
        """
        Initializes the two members the class holds:
        the file name and its contents.
        """
        self.fileName = "None"
        self.fileContent = ""

    def isValid(self, fileName):
        """
        returns True if the file exists and can be
        opened.  Returns False otherwise.
        """
        try:
            file = open(fileName, 'r')
            file.close()
            return True
        except:
            return False

    def setFileName(self, fileName):
        """
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.
        """
        if self.isValid(fileName):
            self.fileName = fileName
            self.fileContents = open(fileName, 'r').read()
        else:
            self.fileContents = ""
            self.fileName = ""

    def getFileName(self):
        """
        Returns the name of the file name member.
        """
        return self.fileName

    def getFileContents(self):
        """
        Returns the contents of the file if it exists, otherwise
        returns an empty string.
        """
        return self.fileContents

    def writeDoc(self, text):
        """
        Writes the string that is passed as argument to a
        a text file with name equal to the name of the file
        that was read, plus the suffix ".bak"
        """
        if self.isValid(self.fileName):
            fileName = self.fileName + ".bak"
            file = open(fileName, 'w')
            file.write(text)
            file.close()

    def upload_cloud(self, filename):

        config = {
            "apiKey": "AIzaSyDxz1w7sZw4PUZAJ-bWbRASpfcBoKwsr84",
            "authDomain": "pre-launch-forecaster.firebaseapp.com",
            "databaseURL": "https://pre-launch-forecaster-default-rtdb.firebaseio.com",
            "projectId": "pre-launch-forecaster",
            "storageBucket": "pre-launch-forecaster.appspot.com",
            "messagingSenderId": "386991533112",
            "appId": "1:386991533112:web:0956fbe12d755d12ea8acd",
            "measurementId": "G-Y2VTVQPWG3",
            "serviceAccount": "serviceAccount.json"
        }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        path_on_cloud = "Datasets/" + filename
        path_local = filename
        print(path_local)
        storage.child(path_on_cloud).put(path_local)

    def getFrom_cloud(self):
        config = {
            "apiKey": "AIzaSyDxz1w7sZw4PUZAJ-bWbRASpfcBoKwsr84",
            "authDomain": "pre-launch-forecaster.firebaseapp.com",
            "databaseURL": "https://pre-launch-forecaster-default-rtdb.firebaseio.com",
            "projectId": "pre-launch-forecaster",
            "storageBucket": "pre-launch-forecaster.appspot.com",
            "messagingSenderId": "386991533112",
            "appId": "1:386991533112:web:0956fbe12d755d12ea8acd",
            "measurementId": "G-Y2VTVQPWG3",
            "serviceAccount": "serviceAccount.json"
        }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        files = storage.list_files()
        names = []
        for file in files:
            listofNames = storage.child(file.name).get_url(None).rsplit('/', 1)[1].replace("%2F", "/").replace(
                "?alt=media", "")
            names.append(listofNames)

        return names

    def downloadDataset(self, fileNAME):
        config = {
            "apiKey": "AIzaSyDxz1w7sZw4PUZAJ-bWbRASpfcBoKwsr84",
            "authDomain": "pre-launch-forecaster.firebaseapp.com",
            "databaseURL": "https://pre-launch-forecaster-default-rtdb.firebaseio.com",
            "projectId": "pre-launch-forecaster",
            "storageBucket": "pre-launch-forecaster.appspot.com",
            "messagingSenderId": "386991533112",
            "appId": "1:386991533112:web:0956fbe12d755d12ea8acd",
            "measurementId": "G-Y2VTVQPWG3",
            "serviceAccount": "serviceAccount.json"
        }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        path_on_cloud = fileNAME
        name_of_file = fileNAME.replace("Datasets/", "")
        print(path_on_cloud, name_of_file)
        storage.child(path_on_cloud).download(name_of_file)
        print('File downloaded')
        print(name_of_file)
        return name_of_file

    def downloadGraph(self,fileNAME):
        config = {
            "apiKey": "AIzaSyDxz1w7sZw4PUZAJ-bWbRASpfcBoKwsr84",
            "authDomain": "pre-launch-forecaster.firebaseapp.com",
            "databaseURL": "https://pre-launch-forecaster-default-rtdb.firebaseio.com",
            "projectId": "pre-launch-forecaster",
            "storageBucket": "pre-launch-forecaster.appspot.com",
            "messagingSenderId": "386991533112",
            "appId": "1:386991533112:web:0956fbe12d755d12ea8acd",
            "measurementId": "G-Y2VTVQPWG3",
            "serviceAccount": "serviceAccount.json"
        }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        path_on_cloud = fileNAME
        name_of_file = fileNAME.replace("Graphs/", "")
        print(path_on_cloud, name_of_file)
        storage.child(path_on_cloud).download(name_of_file)
        print('File downloaded')
        print(name_of_file)
        return name_of_file

    def returnURL(self, imageName):
        config = {
            "apiKey": "AIzaSyDxz1w7sZw4PUZAJ-bWbRASpfcBoKwsr84",
            "authDomain": "pre-launch-forecaster.firebaseapp.com",
            "databaseURL": "https://pre-launch-forecaster-default-rtdb.firebaseio.com",
            "projectId": "pre-launch-forecaster",
            "storageBucket": "pre-launch-forecaster.appspot.com",
            "messagingSenderId": "386991533112",
            "appId": "1:386991533112:web:0956fbe12d755d12ea8acd",
            "measurementId": "G-Y2VTVQPWG3",
            "serviceAccount": "serviceAccount.json"
        }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()

        url = storage.child(imageName).get_url(None)
        return url
