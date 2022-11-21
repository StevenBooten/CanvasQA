import sys
from simple_settings import settings
import progressbar
sys.path.append("../")
from canvaslib.Canvaslib import databaseSearchCanvas, parseArgsCanvas, initialiseLogging
from canvaslib.CanvasAPIClass import CanvasAPI
from Checks.body import checkPageBody
from Gatherers.assessments import collectCourseAssignments
from Gatherers.fileStructure import collectCourseFiles
from Gatherers.moduleInfo import collectCourseModules, unattachedPages, collectCoursePages
from htmlgeneration.canvasQaHtml import generateQaHtml
import json
from pprint import pprint
from pathlib import Path

sys.setrecursionlimit(2000)

def mainProgram():
    
    args, courseDetails, myCanvas = setupVariables()
    
    bar = progressbar.ProgressBar(maxval=len(courseDetails), \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    
    for count, course in enumerate(courseDetails):
        
        canvasQa = {}
        canvasQa['usedFiles'] = []
        canvasQa['issues'] = {}
        
        myCanvas.getCourse(course['canvasCourseId'])
        
        canvasQa['pages'] = collectCoursePages(myCanvas)
        
        canvasQa['modules'], usedFiles = collectCourseModules(myCanvas)
        canvasQa['usedFiles'] += usedFiles
        
        canvasQa['assignments'], usedFiles = collectCourseAssignments(myCanvas)
        canvasQa['usedFiles'] += usedFiles
        
        canvasQa['unattachedPages'] = unattachedPages(myCanvas, canvasQa['modules'], canvasQa['pages'])
        
        canvasQa['pages'], usedFiles = checkPageBody(canvasQa['pages'], myCanvas)
        canvasQa['usedFiles'] += usedFiles
        
        canvasQa['files'], canvasQa['issues']['File Structure'] = collectCourseFiles(myCanvas, canvasQa['usedFiles'])
            
        canvasQaHtml = generateQaHtml(myCanvas, canvasQa)
        saveQaHtml(canvasQaHtml, myCanvas)
        
        with open(f'./jsons/{myCanvas.courseCode} QA.json', 'w') as outfile:
            json.dump(canvasQa, outfile, indent=4)
        
        bar.update(count+1)
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