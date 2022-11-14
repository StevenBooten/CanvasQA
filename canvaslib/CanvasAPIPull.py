from importlib.util import module_for_loader
from os import link
from pydoc import pager
from simple_settings import settings
from canvasapi import Canvas
from sqlalchemy import null
from pprint import pprint
import bs4 as bs
import urllib.request
import requests
from pathlib import Path
import re
class canvasApiPull():
    def __init__(self, courseId):
        self.courseId = courseId
        self.canvasConnection = Canvas(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
        self.course = self.canvasConnection.get_course(self.courseId)
    
    def getFolders(self):
        return self.course.get_folders()
    
    def getCourseCode(self):
        return self.course.course_code
    
    def getSisId(self):
        return self.course.sis_course_id
    
    def getModuleInfo(self):
        return self.course.get_modules()
    
    def getModuleItems(self, moduleId):
        return self.course.get_module(moduleId).get_module_items()
    
    def getPages(self):
        return self.course.get_pages()
    
    def getPage(self, pageId):
        return self.course.get_page(pageId)
    
    def getPageLinks(self, body):
        
        soup = bs.BeautifulSoup(body, features="html.parser")
        links = []
        for link in soup.findAll('a'):
            if link.has_attr('href'):
                #if link.get('href').startswith('..'):
                #    continue
                
                if link.has_attr('id'):
                    links.append([link.get_text(), link.get('href'), link.get('id')])
                else:
                    links.append([link.get_text(), link.get('href'), None])
        for link in soup.findAll('span'):
            if link.has_attr('href'):
                #if link.get('href').startswith('..'):
                #    continue
                
                if link.has_attr('id'):
                    links.append([link.get_text(), link.get('href'), link.get('id')])
                else:
                    links.append([link.get_text(), link.get('href'), None])

        return [links]
    
    def getFileLinks(self, body):
        soup = bs.BeautifulSoup(body, features="html.parser")
        links = []
        for link in soup.findAll('href'):
            if link.get('href').find("https://griffitheduau.sharepoint.com") > -1 or link.get('href').find("https://griffitheduau-my.sharepoint.com") > -1:
                links.append(link.get_text(), link.get('href'))
        return links
    
    def getPageSpanTags(self, body):
        soup = bs.BeautifulSoup(body, features="html.parser")
        spans = []
        for span in soup.findAll('span'):
            if span.has_attr('class'):
                spans.append([span.get_text(), span.get('class')])
        return spans
    
    def getBBEcho(self, body):
        soup = bs.BeautifulSoup(body, features="html.parser")
        echo = []
        for item in soup.findAll('iframe'):
            if item.has_attr('src'):
                if item['src'].find("echo-library-BB5bb") > -1:
                    echo.append(item.get('title'))
        return echo
    
    def getVideoIframes(self, body):
        soup = bs.BeautifulSoup(body, features="html.parser")
        video = []
        for item in soup.findAll('iframe'):
            if item.has_attr('src'):
                video.append(item.get('src'))
                #if item['src'].find("echo-library-BB5bb") > -1:
                #    echo.append(item.get('title'))
        return video
    
    def getBBArtifactTags(self, body):
        soup = bs.BeautifulSoup(body, features="html.parser")
        spans = []
        for span in soup.findAll('div'):
            if span.has_attr('class'):
                if len(span.get('class')) > 0:
                    if span.get('class')[0] == 'vtbegenerated_div':
                        spans.append([span.get_text(), span.get('class')[0]])
        return spans
    
    def getPageMarkTags(self, body):
        soup = bs.BeautifulSoup(body, features="html.parser")
        marks = []
        for mark in soup.findAll('mark'):
            marks.append(re.sub('<[^<]+?>', '', str(mark)))
            #if span.has_attr('class'):
            #    spans.append([span.get_text(), span.get('class')])
        return marks
    
    def getPageImgTags(self, body):
        soup = bs.BeautifulSoup(body, features="html.parser")
        imgs = {}
        for img in soup.findAll('img'):
            if img.has_attr('src'):
                if img.has_attr('id'):
                    imgs[img.get('alt')] = [img.get('src'), img.get('id')]
                else:
                    imgs[img.get('alt')] = [img.get('src'), None]
        return imgs
    
    def getUnattachedPages(self):
        pages = self.getPages()
        unattachedPages = []
        modules = self.getModuleInfo()
        attachedPages = []
        for module in modules:
            items = self.getModuleItems(module.id)
            for item in items:
                attachedPages.append(item.title)
        for page in pages:
            if page.title not in attachedPages:
                if page.url == 'canvas-collections-configuration':
                    continue
                unattachedPages.append(page)
        return unattachedPages
    
    def getFileList(self):
        files = self.course.get_files()
        folders = self.course.get_folders()
        
        return folders, files
    
    def getAssignmentGroups(self):
        return self.course.get_assignment_groups()
    
    def getAssessments(self):
        return self.course.get_assignments()
    
    def getGroupAssignments(self, group):
        return self.course.get_assignments_for_group(group)
    
    def getQuizzes(self):
        return self.course.get_quizzes()
    
    def getQuizQuestions(self, quiz):
        return quiz.get_questions()
    
    def uploadFile(self, filePath, fileName):
        token = self.course.upload(Path(filePath, fileName), parent_folder_path = '/QA Info')
        print(f'{token[1]["upload_status"]}: {fileName}')
        
    def getItemLinks(self, browser):
        
        modules = self.course.get_modules()
        links = []

        for module in modules:
            items = module.get_module_items()
            for item in items:
                if item.type == 'File':
                    browser.get(item.html_url)
                    soup = bs.BeautifulSoup(browser.page_source, features="html.parser")
                    for link in soup.findAll('a'):
                        if link.has_attr('href'):
                            url = link.get('href')
                            try:
                                start = url.index('files/') + 6
                                end = url[start::].index('/')
                                end += start
                                id = url[start:end]
                                links.append(id)
                            except:
                                pass
            
        return links
    
    def getPageText(self, body):
        soup = bs.BeautifulSoup(body, features="html.parser")
        pageText = ''
        
        for page in soup.find_all('p'):
            pageText += page.get_text()
        
        if len(pageText) < 1:
            return 0
        else:
            return len(pageText)
        
    def getTeachers(self):
        
        return self.course.get_enrollments(type='TeacherEnrollment')
    
    def getUser(self, id):
        print(id)
        print(self.course.get_user(id))
        return self.course.get_user(id)
