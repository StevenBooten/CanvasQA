"""
populateCanvasCourseSite.py

- Read entire contents of migration::dev_window_courses table and populate course_site
  based on that data and searching Blackboard 
"""

from ast import JoinedStr
from asyncio.windows_events import NULL
from statistics import multimode
from unicodedata import numeric
from numpy import place
try:
    from simple_settings import settings
except:
    from lib.CanvasSettings import CanvasSettings
    settings = CanvasSettings()
from pathlib import Path
from datetime import datetime


#settings = LazySettings('D:/ael-automation/migration/attendance-db_settings.toml')

from sqlalchemy import create_engine, null, text
import pandas as pd
import argparse
from canvasapi import Canvas
import re



from pprint import pprint

import logging
import sys
sys.path.append("../")
from lib.canvasQAlib import initialiseLogging


#Canvas Account number for each group.
AEL_DEV_ACCOUNT = 106
AEL_GROUP_ACCOUNT = 117
GBS_GROUP_ACCOUNT = 118
HEALTH_GROUP_ACCOUNT = 119
SCIENCE_GROUP_ACCOUNT = 120
OTHER_ACCOUNT = 121


"""
Arguments that can be passed to the script
"""
def parseArgs():
    """Function to parse command line arguments
    - username/password (optional) for Blackboard 
      will default to settings
    
    :returns: args dict of arguments, keyed on value
    """
    parser = argparse.ArgumentParser(
        description="Scrape and pickle a description of Blackboard course site")

    #parser.add_argument("dw",action="store",help="Dev window integer (1=T3, 2=T1, 3=T3)")
    parser.add_argument("--username", action="store", default=settings.BB_USERNAME)
    parser.add_argument("--password", action="store", default=settings.BB_PASSWORD)
    parser.add_argument('--group', action='store', default='AEL')
    parser.add_argument('--dev', action='store_true', default=False)
    

    args = parser.parse_args()

    return args



"""
Fields for Database

FIELD                                                                   EXAMPLE
'CourseInstanceId' = sis_course_id                                      1003CCJ-3228-*-*
'course' = sis_course_id (split)                                        1003CCJ
'year' = sis_course_id (split)                                          2022
'period' = sis_course_id (split)                                        8
'termCode' = sis_course_id (split)                                      3228
'uniGroup' = group                                                      'AEL'                                     
'campus' = sis_course_id (split)                                        *-*
'canvasCourseId' = id                                                   4299
'courseSiteUrl' = settings.COURSE_URL / id                              lms.griffith.edu.au/course/4299
'accountId' = account_id int turned into str 106=DEV 117=Live           Live
'workflowStatus' = workflow_state                                       unpublished
'defaultView' = default_view                                            wiki
'oua' = if coursecode starts with a letter instead of number            1 or 0
'collectionDate' = now                                                  22-06-2022 14:32


"""
def insertCourseSites(entries):
    """Function to insert new entries into canvas_course_sites

    :param entries: list of dicts containing entries to insert
    """
    
    database = f"sqlite:///{settings.MIGRATION_DATABASE}"

    engine = create_engine(database, echo=False)

    connection = engine.connect()

    query = text("""INSERT into canvas_course_sites values(:courseInstanceId, :course, :year, :period, :termCode, :uniGroup, :school, :campus, :canvasCourseId, :courseSiteUrl, :accountId, :oua, :workflowStatus, :defaultView, :collectionDate, :retired, :LearningJourney, :AssessmentOverview, :StaffPage, :joined)""")
    message = f'Adding {entries["courseInstanceId"]} entries in canvas_course_sites'
    logging.info("************** updating  ***************")
    logging.info(message)
    print(message)
    logging.info(entries)
    result = connection.execute(query, entries)
    logging.info(result)
    logging.info("****************************************")

    connection.close()

    
def getStringValues(start, idString):
    if start != 0:
        start +=1
        
    if start == len(idString):
        return len(idString), len(idString)
    
    if re.search("[_]P[0-9][_]", idString[start::]):
        end = re.search("[_]P[0-9][_]", idString[start::]).start()
        end += start + 3
    elif re.search("[_]Y[0-9][_]", idString[start::]):
        end = re.search("[_]Y[0-9][_]", idString[start::]).start()
        end += start + 3
    elif idString[start::].find('_') > 0:
        end =idString[start::].find('_')
        end += start
    elif idString[start::].find('-') > 0:
        end = idString[start::].find('-')  
        end += start
    elif idString[start::].find('.') > 0:
        end =idString[start::].find('.')
        end += start   
    else:
        end = len(idString)
    return start, end

"""
Takes the course site and puts relavent infomation into a dictionary which is returns
"""
def addCoursetoDict(course, sisid, joined=False):
    start, end = 0, 0
    courseDict = {}
    
    if joined:
        sisCourseId = sisid[0]
    else:
        sisCourseId = sisid
    
    courseDict['courseInstanceId'] = course.sis_course_id.replace('.*.*', '')

    """Dev Shell sis_course_id is set out slightly differently to Live courses"""
    if course.account_id == 106:
        #start, end = getStringValues(end, sisCourseId)
        courseDict['accountId'] = 'DEV' #sisCourseId[start:end:]
        end = 3
        start, end = getStringValues(end, sisCourseId)
        courseDict['course'] = sisCourseId[start:end:]
        start, end = getStringValues(end, sisCourseId)
        courseDict['termCode'] = sisCourseId[start:end:]
        start, end = getStringValues(end, sisCourseId)
        if start == len(sisCourseId):
            courseDict['campus'] = NULL
        else:
            courseDict['campus'] = sisCourseId[start:end:]
    else:
        courseDict['accountId'] = 'Live'
        start, end = getStringValues(end, sisCourseId)
        courseDict['course'] = sisCourseId[start:end:]
        if joined:
            for item in sisid[1::]:
                e = 0
                s, e = getStringValues(e, item)
                courseDict['course'] += f"\n{item[s:e:]}"
            
            
        start, end = getStringValues(end, sisCourseId)
        courseDict['termCode'] = sisCourseId[start:end:]
        start, end = getStringValues(end, sisCourseId)
        courseDict['campus'] = sisCourseId[start::]
    if re.match('^[A-Z][A-Z][A-Z]', courseDict['course'], re.IGNORECASE):
        courseDict['oua'] = 1
    else:
        courseDict['oua'] = 0
    
    courseDict['school'] = re.sub('[0-9]', '', courseDict['course'])[:3]
    courseDict['year'], courseDict['period'] = str('20' + courseDict['termCode'][1:3]), courseDict['termCode'][3:4]
    courseDict['canvasCourseId'] = course.id
    courseDict['courseSiteUrl'] = settings.CANVAS_COURSE_URL + str(courseDict['canvasCourseId'])
    courseDict['workflowStatus'] = course.workflow_state
    courseDict['defaultView'] = course.default_view
    courseDict['collectionDate'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if joined:
        courseDict['joined'] = 1
    else:
        courseDict['joined'] = NULL
    courseDict['retired'] = NULL
    courseDict['LearningJourney'] = NULL
    courseDict['AssessmentOverview'] = NULL
    courseDict['StaffPage'] = NULL
    if course.account_id == 106:
        courseDict['uniGroup'] = 'AEL'
    elif course.account_id == 117:
        courseDict['uniGroup'] = 'AEL'
    elif course.account_id == 120:
        courseDict['uniGroup'] = 'SCG'
    elif course.account_id == 118:
        courseDict['uniGroup'] = 'GBS'
    elif course.account_id == 119:
        courseDict['uniGroup'] = 'HTH'
    elif course.account_id == 121:
        courseDict['uniGroup'] = 'OTH'
    
    return courseDict    
"""
Pulls course information via the Canvas API to add to the course database.
Slightly different codes between dev shells and live shells.

Stores everything in a dictionary inside of a list before sending the list to the insertCourseSites function.
"""
def populateCourseSite(accountInput):
    
    canvas = Canvas(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
    
    entries = {}
    account = canvas.get_account(accountInput)
    courses = account.get_courses()
    #for x in range(155,10000):
    #for x in range(155,endCourseRange):
    
    for course in courses:
        
        try:
            if course.sis_course_id.find('sample') >= 0: #3294 3294
                logging.info('Skipping sample course %s', course.name)
                continue
        except:
            pass
            
        try:
            sisCourseId = course.sis_course_id
            logging.info('Found sis course ID %s', course.sis_course_id)
        except:
            logging.info("No SIS course ID for %s", course.name)
            continue
        
        if course.sis_course_id == None:
            logging.info('Sis course ID is %s, skipping', course.sis_course_id)
            continue
        
        if course.sis_course_id.find('+') > 0 and len(course.sis_course_id) > 16:
            multiCourseId = course.sis_course_id.split('+')
            
            entries[course.id] = addCoursetoDict(course, multiCourseId, joined=True)
        elif course.sis_course_id.find('-') > 0 and len(course.sis_course_id) > 16:
                multiCourseId = course.sis_course_id.split('-')
                entries[course.id] = addCoursetoDict(course, multiCourseId, joined=True)
        else:
            entries[course.id] = addCoursetoDict(course, sisCourseId)
                
                
    return entries
 
def getDatabaseEntries(uniGroup, dev=False):
    database = f"sqlite:///{settings.MIGRATION_DATABASE}"

    engine = create_engine(database, echo=False)
    connection = engine.connect()

    query = (f"select * from canvas_course_sites where uniGroup = '{uniGroup}' or uniGroup is NULL")
    
    
    if dev:
        query += f" and accountId='DEV'"
    else:
        query += f" and accountId='Live'"

    entries = pd.read_sql(query, connection).to_dict("records")
    courseList = {}
    for entry in entries:
        courseList[entry['canvasCourseId']] = entry
    connection.close()
    
    return courseList

def compareAndUpdate(sourceEntry, databaseEntry):
    """Compare a subset of fields in entries for the same course from
    the spreadsheet and database. if there are any changes, update the database 
    entry
    """

    COMPARE_FIELDS={"courseInstanceId":"courseInstanceId", "course":"course", "year":"year", "period":"period",
                    "termCode":"termCode", "uniGroup":"uniGroup", "school":"school", "campus":"campus", "canvasCourseId":"canvasCourseId",
                    "courseSiteUrl":"courseSiteUrl", "accountId":"accountId", "oua":"oua", "workflowStatus":"workflowStatus", 
                    "defaultView":"defaultView", "joined":"joined"}

    updates = {}
    for sFieldName in COMPARE_FIELDS:
        #-- make sure we can get all the datafields
        dFieldName = COMPARE_FIELDS.get(sFieldName, None)
        if dFieldName==None:
            logging.error(f"ERROR no matching database fieldname for {sFieldName}")
            continue

        sField = sourceEntry.get(sFieldName,None)
        if sField==None:
            logging.warning(f"ERROR no {sFieldName} in sourceEntry")
            sField = ""
        dField = databaseEntry.get(dFieldName,None)
        if dField==None:
            #-- databaase value is empty, set it empty and compare
            logging.warning(f"ERROR no {dFieldName} in databaseEntry set to empty")
            dField = ""

#        print(f"comparing {sFieldName}:{sField} with {dFieldName}:{dField}")

        #-- compare the fields
        if sField != dField:
#            print("------------ DIFFERENCE")
            # if different, add entry to updates
            # - key is the database fieldname
            # - value is the new value from the spreadsheet
            updates[dFieldName] = sField
            
    #-- if updates dict is not empty, update the database
    if len(updates.keys())>0:

        logging.info(f"Updating {databaseEntry['courseInstanceId']}")

        updateCanvasCourse(databaseEntry["courseInstanceId"], updates)

def updateCanvasCourse(courseCode, updates):
    """Update the entry for a course in dev_window_courses

    :param courseCode: which row (courseCode) to update
    :param updates: dict specifying the fields/values to update
    """

    database = f"sqlite:///{settings.MIGRATION_DATABASE}"

    engine = create_engine(database, echo=False)
    connection = engine.connect()

    updateString = ""
    for key, value in updates.items():
        updateString += f"\"{key}\"='{value}',"

    #-- remove trailing comma
    if "," in updateString: 
        updateString = updateString[:-1]

    query = (
        f"update canvas_course_sites set {updateString} where " +
        f"courseInstanceId='{courseCode}'" )
    

    #print(f"{query = }")

    try: 
        connection.execute(query)
    except Exception as e:
        logging.error(f"Error updating course: {e}")

    connection.close()

def main():
    args = parseArgs() 

    initialiseLogging('Canvas Populate Course Site.log')
    logging.info(f"***** Commencing populateCanvasCourseSites *****")
    startTime = datetime.now()
    
    
    if args.group == 'AEL' and args.dev:
        account = [AEL_DEV_ACCOUNT]
    elif args.group == 'AEL' and not args.dev:
        account = [AEL_GROUP_ACCOUNT]
    elif args.group == 'SCG':
        account = [SCIENCE_GROUP_ACCOUNT]
    elif args.group == 'GBS':
        account = [GBS_GROUP_ACCOUNT]
    elif args.group == 'HTH':
        account = [SCIENCE_GROUP_ACCOUNT]
    elif args.group == 'OTH':
        account = [OTHER_ACCOUNT]

        
    sourceEntries = populateCourseSite(account)
    databaseEntries = getDatabaseEntries(args.group, args.dev)
    
    for key, sourceEntry in sourceEntries.items():
        databaseEntry = databaseEntries.get(key, None)
        if databaseEntry == None:
            logging.info(f"Adding new course {sourceEntry['course']}")
            insertCourseSites(sourceEntry)
        else:
            compareAndUpdate(sourceEntry, databaseEntry)
        
        #UpdateCourseSites(entries)
    #populateCourseSite(args)
    endTime = datetime.now()
    print(f'time taken: {endTime - startTime}')


if __name__ == '__main__': 
    main()
