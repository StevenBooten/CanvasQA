import requests
import re
#from simple_settings import settings
from lib.CanvasSettings import CanvasSettings
settings = CanvasSettings()


TIMEOUT = 20
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
    #'Accept-Encoding' : '*',
    #'Connection' : 'keep-alive',
    'Authorization' : settings.CANVAS_API_KEY,
    #'Content-Type' : 'application/json',
    #'accept' : 'application/json'
}

def validate_url(url):
    
    """ import json
    try:
        browser.get(url)
    
        for entry in browser.get_log('performance'):
            for k, v in entry.items():
                if k == 'message' and 'status' in v:
                    msg = json.loads(v)['message']['params']
                    for mk, mv in msg.items():
                        if mk == 'response':
                            response_url = mv['url']
                            response_status = mv['status']
                            if response_url == url:
                                return response_status
    except:
        pass"""
    status = 0
    try:
        r = requests.head(url, timeout=TIMEOUT, headers=REQUEST_HEADERS)
        status = r.status_code
    except Exception as e:
        pass

    return status
         
        
def linkCheck(url, myCanvas):
    
    badLink = 1
    goodLink = 0
    
    if '@X@EmbeddedFile.requestUrlStub/' in url.lower():
        return 999, badLink
    elif 'webapps/echo-library' in url.lower():
        return 999, badLink
    elif 'bbcollab' in url.lower():
        return 999, badLink
    elif 'bblearn' in url.lower():
        return 999, badLink
    elif 'blackboard' in url.lower():
        return 999, badLink
    elif 'EmbeddedFile.request' in url.lower():
        return 999, badLink
    elif 'mailto' in url.lower():
        return 298, goodLink
    elif 'https://griffitheduau.sharepoint.com' in url.lower():
        return 297, goodLink
    elif 'tel:' in url.lower():
        return 296, goodLink
    
    #added for Jtool recognition.
    if 'app.secure.griffith' in url.lower() and '@user.id@' in url.lower():
        return 998, badLink
    
    elif url.lower().startswith('#'):
        return 299, goodLink
    
    start = re.match('https://lms.griffith.edu.au/courses/', url.lower())
    if start is not None:
        end = re.match('/[a-z]*', url.lower()[start.end()::])
        if end is not None:
            courseId = url.lower()[start.end():end.start()]
            if courseId != myCanvas.courseId:
                return 322, badLink
            
    
    statusCode = validate_url(url)
    
    if statusCode < 400 or statusCode >= 300:
        if url.lower().startswith('http://'):
            return 398, badLink
        
    if statusCode == 302:
        if url.lower().startswith('https://lms.griffith.edu.au/'):
            statusCode = 200
    
    if statusCode < 200:
        return statusCode, badLink  
    elif statusCode < 300:
        return statusCode, goodLink
    else:
        return statusCode, badLink
    
    