import requests
import re
from simple_settings import settings


TIMEOUT = 20
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Authorization' : settings.CANVAS_API_KEY
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
    
    if '@X@EmbeddedFile.requestUrlStub/' in url:
        return 999
    elif 'bbcollab' in url:
        return 999
    elif 'blackboard' in url:
        return 999
    elif 'EmbeddedFile.request' in url:
        return 999
    elif 'mailto' in url:
        return 298
    elif 'https://griffitheduau.sharepoint.com' in url:
        return 297
    elif 'tel:' in url:
        return 296
    
    start = re.match('https://lms.griffith.edu.au/courses/', url)
    if start is not None:
        end = re.match('/[a-z]*', url[start.end()::])
        if end is not None:
            courseId = url[start.end():end.start()]
            if courseId != myCanvas.courseId:
                return 222
            
    
    
    statusCode = validate_url(url)
    
    if statusCode < 399 or statusCode < 300:
        if 'http://' in url:
            return 998
        
    return statusCode