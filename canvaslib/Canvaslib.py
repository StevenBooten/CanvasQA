try:
    from simple_settings import settings
except:
    from lib.CanvasSettings import CanvasSettings
    settings = CanvasSettings()
from canvasapi import Canvas
from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path
from pycanvas.apis.pages import PagesAPI
from pycanvas.apis.enrollments import EnrollmentsAPI
from pycanvas.apis.courses import CoursesAPI
from bs4 import BeautifulSoup as bs
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import argparse
import logging

def getDevWindowCourse(course):
    """
    Obtain matching rows from the dev_widow_courses table
    but only get courses that haven't been retired from this devWindow
    """

    database = f"sqlite:///{settings.MIGRATION_DATABASE}"

    engine = create_engine(database, echo=False)
    connection = engine.connect()

    query = (
        "select * from dev_window_courses WHERE" +
        " ( retired is NULL or retired=0 ) and" +
        " CourseCode = '{}'".format(course)
    )

    entries = pd.read_sql(query, connection).to_dict("records")
    connection.close()
    
    

    return entries

def canvasLogin(browser, courseId=3294):
    
    url = f'https://lms.griffith.edu.au/courses/{courseId}/'
    browser.get(url)
    
    try:
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email'][@name='loginfmt']")))
        browser.find_element( By.XPATH, "//input[@type='email'][@name='loginfmt']" ).send_keys(settings.EMAIL_ADDRESS)
    except:
        raise Exception("enterGriffithEcho360: Couldn't find input#email")
    
    try:
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
        browser.find_element( By.ID, 'idSIButton9' ).click()
    except:
        raise Exception("enterGriffithEcho360: Couldn't find input#email")
    time.sleep(5)
    try:
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "idBtn_Back")))
        browser.find_element( By.ID, "idBtn_Back").click()
    except:
        raise Exception("enterGriffithEcho360: Couldn't find input#email")
    
    
    return browser


def getCanvasCourseList(group, accountId, oua = False, org = False, school = None, term = None, year = None, course = None, ignoreJoined = False):
    database = f"sqlite:///{settings.MIGRATION_DATABASE}"

    engine = create_engine(database, echo=False)
    connection = engine.connect()

    query = (f"select * from canvas_course_sites where uniGroup='{group}'")
    
    if accountId is not None:
        query += f" and accountId='{accountId}'"
    
    if oua:
        query += f" and oua=1"
        
    if org:
        query += f" and org=1"
        
    if school is not None:
        query += f" and school='{school}'"
        
    if year is not None:
        query += f" and year='{year}'"
        
    if term is not None:
        if len(term.split('-')) > 1:
            query += ' and ('
            for term in term.split('-'):
                query += f" termCode='{term}' or"
            query = query[:-3]
            query += ')'
        else:
            query += f" and termCode='{term}'"
    
    if course is not None:
        query += f" and course like '%{course}%'"
        
    query += ' and (retired=0 or retired is null)'
    
    if ignoreJoined:
        query += ' and (joined=0 or joined is null)'

    courseList = pd.read_sql(query, connection).to_dict("records")
    connection.close()
    
    return courseList

def updateWhyFramePopulateDate(courseInstanceId, whyframeName):
    """Update the dateScraped field for a course_sites entry

    :param courseInstanceId: courseInstanceId to update
    :param dateScraped: date to update to
    """

    database = f"sqlite:///{settings.MIGRATION_DATABASE}"

    engine = create_engine(database, echo=False)
    connection = engine.connect()
    dateScraped = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = (
        f"update canvas_course_sites set {whyframeName}='{dateScraped}' where courseInstanceId='{courseInstanceId}'"
    )

    connection.execute(query)

    connection.close()

def pageCharCheck(canvasCourseId, pageId, charCheckSize):
    canvasConnection = Canvas(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
    course = canvasConnection.get_course(canvasCourseId)
    
    page = course.get_page(pageId)
    
    soup = bs(page.body, features="html.parser")
    
    pageText = ''
    
    for page in soup.find_all('p'):
        pageText += page.get_text()
    
    if len(pageText) < charCheckSize:
        return 1
    else:
        return 0

def findPageUrl(canvasCourseId, searchPage):
    canvasConnection = Canvas(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
    course = canvasConnection.get_course(canvasCourseId)

    for page in course.get_pages():
        
        if page.title == searchPage:
            return page.url
        
def findPageId(canvasCourseId, searchPage):
    canvasConnection = Canvas(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
    course = canvasConnection.get_course(canvasCourseId)

    for page in course.get_pages():
        
        if page.title == searchPage:
            return page.page_id
        
def updateCanvasPage(canvasCourseUrl, canvasCourseId, body):
    myPage = PagesAPI(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
    return myPage.update_create_page_courses(canvasCourseUrl, canvasCourseId, wiki_page_body=body)
    
def createCanvasPage(pageTitle, canvasCourseId, body):
    myPage = PagesAPI(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
    return myPage.create_page_courses(canvasCourseId, pageTitle, wiki_page_body=body)


def parseArgsCanvas():
        
    parser = argparse.ArgumentParser(
        description="Generate HTML to go into Canvas course sites")
    
    # These arguments as of November 2022 are used just for the canvas wireframe tools
    parser.add_argument('--learning', action="store_true", default=False)
    parser.add_argument('--assessment', action="store_true", default=False)
    parser.add_argument('--teacher', action="store_true", default=False)
    parser.add_argument('--list', action="store_true", default=False)
    parser.add_argument('--tabbed', action="store_true", default=False)
    parser.add_argument('--normal', action="store_true", default=False)
    parser.add_argument('--ignoreCharCheck', action="store_true", default=False)
    parser.add_argument('--css', action="store_true", default=False)
    parser.add_argument('--update', action="store_true", default=False)
    
    # These arguments are used for all canvas tools that save something.
    parser.add_argument("--folder", action="store", default=settings.CANVAS_FOLDER)
    
    parser.add_argument('--loop', action="store_true", default=False)
    parser.add_argument('--count', action="store", default=0)
    
    #these arguments are used for all canvas tools to be able to specify whatever consort of courses you want
    parser.add_argument("--group", action='store', default='AEL', help="school to obtain courses from")
    parser.add_argument('--accountId', action="store", default='Live')
    parser.add_argument('--course', action="store", default=None)
    parser.add_argument('--oua', action="store_true", default=False)
    parser.add_argument('--org', action="store_true", default=False)
    parser.add_argument('--school', action="store", default=None)
    parser.add_argument('--ignoreJoined', action="store_true", default=False)
    parser.add_argument('--term', action="store", default=None)
    parser.add_argument('--year', action="store", default=None)
    
    #these arguments are used for small runs of Canvas QA without needing any sort of database
    parser.add_argument('--url', action="store", default=None)
    parser.add_argument('--spreadsheet', action="store", default=None)
    
    return parser.parse_args()
    

def databaseSearchCanvas(group, status, oua = False, org = False, school = None, courseList = None, list = None, term = None, year = None, course = None, ignoreJoined = False):
    
    if list:
        courseDetails = []
        for course in courseList:
            course = getCanvasCourseList(group, status, oua=oua, org=org, school=school, term=term, year=year, course=course, ignoreJoined=ignoreJoined)
            courseDetails.append(course[0])
#    elif course != None:
#        courseDetails = getCanvasCourseList(group, status, oua=oua, school=school, term=term, year=year, course=course, ignorejoined=ignoreJoined)
    else:
        courseDetails = getCanvasCourseList(group, status, oua=oua, org=org, school=school, term=term, year=year, course=course, ignoreJoined=ignoreJoined)
        
    return courseDetails


def initialiseLogging(logFileName=None):
    """Set up basic logging information for all CAR generation
    Use default MIGRATION_LOGFILE unless filename specified
    Specified log file is just a name used with MIGRATION_BASE
    """

    if logFileName is None:
        logFileName = settings.MIGRATION_LOGFILE
    else:
        logFileName = f"{settings.LOGS}{logFileName}"

    logging.basicConfig( level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(filename)s %(funcName)s %(lineno)d: %(message)s',
        filename=logFileName )

def getTeachingSection(sections):
    for section in sections:
        if section.name.startswith('Teaching Team'):
            return section.id
    
def enrolUser(user, canvasCourseId, enrollmentType, sectionId):
    myEnrollment = EnrollmentsAPI(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
    return myEnrollment.enroll_user_courses(course_id=canvasCourseId, enrollment_type=enrollmentType, enrollment_user_id=user, enrollment_enrollment_state='active', enrollment_course_section_id=sectionId)

def removeUser(user, canvasCourseId):
    myEnrollment = EnrollmentsAPI(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
    return myEnrollment.conclude_deactivate_or_delete_enrollment(course_id=canvasCourseId, id=user, task="delete")
    
def publishCourse(canvasCourseId, courseEvent):
    myCourse = CoursesAPI(settings.CANVAS_API_URL, settings.CANVAS_API_KEY)
    return myCourse.update_course(canvasCourseId, course_event=canvasCourseId)