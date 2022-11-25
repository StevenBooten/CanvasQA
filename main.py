import sys
from simple_settings import settings
import progressbar
sys.path.append("../")
from canvaslib.Canvaslib import databaseSearchCanvas, parseArgsCanvas, initialiseLogging
from canvaslib.CanvasAPIClass import CanvasAPI
from Checks.body import checkPageBody
from Gatherers.assignments import collectCourseAssignments
from Gatherers.fileStructure import collectCourseFiles
from Gatherers.moduleInfo import collectCourseModules, unattachedPages, collectCoursePages
from htmlgeneration.canvasQaHtml import generateQaHtml
import json
from pprint import pprint
from pathlib import Path

sys.setrecursionlimit(2000)

MAXBAR = 100
def updateBar(count, bar):
    step = MAXBAR / 8 #This is the number of steps in the main program
    
    count += 1
    
    bar.update((MAXBAR/step) * count)

def mainProgram():
    
    args, courseDetails, myCanvas = setupVariables()
    
    
    for course in courseDetails:
        count = 1
        canvasQa = {}
        canvasQa['usedFiles'] = []
        canvasQa['issues'] = {}
        canvasQa['issues']['Images'] = { 'id':"collapsible-img-check", 'count' : 0, 'html' : ''}
        canvasQa['issues']['Assignments'] = { 'id':"collapsible-assignment-check", 'count' : 0, 'html' : '' }
        canvasQa['issues']['Blackboard Residuals'] = { 'id':"collapsible-bb-check", 'count' : 0, 'html' : '' }
        canvasQa['issues']['File Structure'] = {'id': "collapsible-filestructure-check", 'count' : 0, 'html' : '' }
        canvasQa['issues']['Modules'] = { 'id':"collapsible-modules-check", 'count' : 0, 'html' : '' }
        canvasQa['issues']['Placeholders'] = { 'id':"collapsible-placeholder-check", 'count' : 0, 'html' : '' }
        canvasQa['issues']['Unattached Pages'] = { 'id':"collapsible-unattachedpages-check", 'count' : 0, 'html' : '' }
        canvasQa['issues']['Course Links'] = { 'id':"collapsible-link-check", 'count' : 0, 'html' : '' }
        canvasQa['issues']['Embedded Content'] = { 'id':"collapsible-video-check", 'count' : 0, 'html' : ''}
        
        myCanvas.getCourse(course['canvasCourseId'])
        print(f'Running: {myCanvas.courseCode}')
        bar = progressbar.ProgressBar(maxval=MAXBAR, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        
        bar.start()
        canvasQa['pages'] = collectCoursePages(myCanvas)
        updateBar(count, bar)
        
        canvasQa['usedFiles'] += collectCourseModules(myCanvas, canvasQa)
        updateBar(count, bar)
        
        usedFiles = collectCourseAssignments(myCanvas, canvasQa)
        canvasQa['usedFiles'] += usedFiles
        updateBar(count, bar)
        
        canvasQa['unattachedPages'] = unattachedPages(myCanvas, canvasQa)
        updateBar(count, bar)
        
        usedFiles = checkPageBody(canvasQa, myCanvas)
        canvasQa['usedFiles'] += usedFiles
        updateBar(count, bar)
        
        canvasQa['files'] = collectCourseFiles(myCanvas, canvasQa)
        updateBar(count, bar)
        
        with open(f'./jsons/{myCanvas.courseCode} QA.json', 'w') as outfile:
            json.dump(canvasQa, outfile, indent=4)
        updateBar(count, bar)
            
        canvasQaHtml = generateQaHtml(myCanvas, canvasQa)
        saveQaHtml(canvasQaHtml, myCanvas)
        updateBar(count, bar)
        
        
        
        bar.finish()
    
def saveQaHtml(canvasQaHtml, myCanvas):
    
    filePath = f'{settings.CANVAS_QA_DOWNLOAD_FOLDER}'
    fileName = f'{myCanvas.courseCode.replace("_"," ").replace("/", "-").replace(":", "-").replace("?", "")} QA.html'
    
    # uploads the HTML report to the canvas course site
    with open(Path(filePath, fileName), 'w', encoding="utf-8") as f:
        f.write(canvasQaHtml.render(pretty=True, doctype=True))
    

def setupVariables():
        
    initialiseLogging("Canvas QA.log")
    
    args = parseArgsCanvas()   
    
    courseList = ['7917QCA']
        
    courseDetails = databaseSearchCanvas(args.group, args.accountId, courseList=courseList, oua=args.oua, list=args.list, term=args.term, year=args.year, course=args.course, ignoreJoined=args.ignoreJoined)
    
    return args, courseDetails, CanvasAPI()
       
        
    
if __name__ == '__main__':
    
    mainProgram()