
try:
    from simple_settings import settings
except:
    from lib.CanvasSettings import CanvasSettings
    settings = CanvasSettings()
from canvasapi import Canvas
from pathlib import Path

class CanvasAPI():
    def __init__(self):
        self.canvasConnection = Canvas(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
        self.course = None
        self.courseId = None
        
    def getCourse(self, courseId, include=None):
        self.courseId = courseId
        if include is None:
            self.course = self.canvasConnection.get_course(self.courseId)
        else:
            self.course = self.canvasConnection.get_course(self.courseId, include=include)
        self.courseCode = self.course.sis_course_id
        
    def getTeachers(self):
        return self.course.get_enrollments(type='TeacherEnrollment')
    
    def getModules(self):
        return self.course.get_modules()
    
    def getModuleItems(self, moduleId):
        return self.course.get_module(moduleId).get_module_items()
    
    def getAssignmentGroups(self, include):
        return self.course.get_assignment_groups(include=include)
    
    def getAssignment(self, id, include=None):
        return self.course.get_assignment(id, include=include)
    
    def getQuiz(self, quizId):
        return self.course.get_quiz(quizId)
    
    #def getGroupAssignments(self, group):
    #    return self.course.get_assignments_for_group(group)
    
    def getPages(self):
        return self.course.get_pages()
    
    def getDesigners(self):
        return self.course.get_enrollments(type='DesignerEnrollment')
    
    def getTA(self):
        return self.course.get_enrollments(type='TaEnrollment')
    
    def getStudents(self):
        return self.course.get_enrollments(type='StudentEnrollment')
    
    def getFileFolders(self):
        return self.course.get_folders()
    
    def getUser(self, id):
        return self.course.get_user(id)
    
    def getPages(self):
        return self.course.get_pages()
    
    def getPage(self, pageId):
        return self.course.get_page(pageId)
    
    def getFile(self, fileId):
        return self.course.get_file(fileId)
    
    def downloadFile(self, file, location):
        return file.download(location)
    
    def getFiles(self):
        return self.course.get_files()
    
    def uploadFile(self, filePath, fileName, parentFolder):
        token = self.course.upload(Path(filePath, fileName), parent_folder_path = parentFolder)
        return f'{token[1]["upload_status"]}: {fileName}'
    
    def getTabs(self):
        return self.course.get_tabs()
    
    def getWorkflowStatus(self):
        return self.course.workflow_state
    
    def getSections(self):
        return self.course.get_sections() 
    
    def updateCourse(self, **kwargs):
        return self.course.update(**kwargs)
    
    def getAccounts(self):
        return self.canvasConnection.get_accounts()

    