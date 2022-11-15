import sys
from simple_settings import settings
import progressbar
sys.path.append("../")
from canvaslib.Canvaslib import databaseSearchCanvas, parseArgsCanvas, initialiseLogging
from canvaslib.CanvasAPIClass import CanvasAPI
from Checks import body, linkCheck
from Gatherers import fileStructure, moduleInfo
import json
from pprint import pprint

def mainProgram():
    
    args, courseDetails, myCanvas = setupVariables()
    
    canvasQa = {}
    
    bar = progressbar.ProgressBar(maxval=len(courseDetails), \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    
    for count, course in enumerate(courseDetails):
        
        myCanvas.getCourse(course['canvasCourseId'])
        
        canvasQa['pages'] = moduleInfo.collectCoursePages(myCanvas)
        
        canvasQa['modules'], canvasQa['usedFiles'] = moduleInfo.collectCourseModules(myCanvas)
        
        canvasQa['unattachedPages'] = moduleInfo.unattachedPages(myCanvas, canvasQa['modules'], canvasQa['pages'])
        
        canvasQa['pages'] = body.checkPageBody(canvasQa['pages'])
        
        canvasQa['files'] = fileStructure.collectCourseFiles(myCanvas, canvasQa['usedFiles'])
        
        with open(f'./jsons/{myCanvas.courseId} QA.json', 'w') as outfile:
            json.dump(canvasQa, outfile, indent=4)
        
        bar.update(count+1)
    bar.finish()
    
    


def setupVariables():
        
    initialiseLogging("Canvas QA.log")
    
    args = parseArgsCanvas()   
    
    courseList = ['7917QCA']
        
    courseDetails = databaseSearchCanvas(args.group, args.accountId, courseList=courseList, oua=args.oua, list=args.list, term=args.term, year=args.year, course=args.course, ignoreJoined=args.ignoreJoined)
    
    return args, courseDetails, CanvasAPI()
       
        
    
if __name__ == '__main__':
    
    mainProgram()