#This class is created to hold all the settings variables that are normally controlled by simple_settings.
#If you don't have simple_settings or a valid settings.toml file this class will instantiate 

class CanvasSettings:
    def __init__(self) -> None:
        #The url of your canvas site. ie 'http://lms.griffith.edu.au/'
        self.CANVAS_API_URL = ''
        #Your personal access token for the canvas site. 
        #How to can be found here: https://www.youtube.com/watch?v=cZ5cn8stjM0
        self.CANVAS_API_KEY = ''
        #this is the folder the local copy of the QA document is saved. ie. 'c:\\Canvas\\QA\\'
        self.CANVAS_QA_DOWNLOAD_FOLDER = ''
        #This is the folder where your course spreadsheet will be located. ie 'c:\\Canvas\\'
        self.CANVAS_FOLDER = ''
        #The location of where the log file is saved. ie 'c:\\Canvas\\logs\\'
        self.MIGRATION_BASE = ''
        #default log file name and location. ie 'c:\\Canvas\\logs\\QA.log'
        self.MIGRATION_LOGFILE = ''
        #If you are managing your own course Database point to it here. ie 'c:\\Canvas\\Database\\canvasCourses.db'
        self.MIGRATION_DATABASE = ''
        #The email address connected to your canvas account. ie s.booten@griffith.edu.au
        self.EMAIL_ADDRESS = ''
        
        