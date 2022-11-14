import sys
from simple_settings import settings
import progressbar
sys.path.append("../")
from canvaslib.Canvaslib import databaseSearchCanvas, parseArgsCanvas, initialiseLogging
from canvaslib.CanvasAPIClass import CanvasAPI

def mainProgram():
    
    args, courseDetails, myCanvas = setupVariables()
    
    kwargs = {}
    
    bar = progressbar.ProgressBar(maxval=len(courseDetails), \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    
    for count, course in enumerate(courseDetails):
        myCanvas.getCourse(course['canvasCourseId'], **kwargs)
        
        
        
        bar.update(count+1)
    bar.finish()


def setupVariables():
        
    initialiseLogging("wireframe generation.log")
    
    args = parseArgsCanvas()   
    
    courseList = ['7917QCA']
        
    courseDetails = databaseSearchCanvas(args.group, args.accountId, courseList=courseList, oua=args.oua, list=args.list, term=args.term, year=args.year, course=args.course, ignoreJoined=args.ignoreJoined)
    
    return args, courseDetails, CanvasAPI()
       
        
    
if __name__ == '__main__':
    
    mainProgram()