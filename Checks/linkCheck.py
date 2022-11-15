import requests


TIMEOUT = 20
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0'
}

def validate_url(url, browser):
    
    if url.find('blackboard') > -1:
        return 999
    elif url.find('EmbeddedFile.request') > -1:
        return 999
    elif url.find('bbcollab') > -1:
        return 999
    
    import json
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
        pass
    status = 0
    #description = ""
    try:
        r = requests.head(url, timeout=TIMEOUT, headers=REQUEST_HEADERS)
        status = r.status_code
        #description = http.client.responses[status]
        #print(f"--- checked {link} --- {r.status_code}")
    except Exception as e:
        pass
        #print(f".. exception {e}")
        #description = f"error {e}"

    return status
        
def imgLinkCheck(browser, qaInfo, imageTags, pageTitle, pageUrl, quizpage = False):  
    
    for altTag, imgList in imageTags.items():
        imgLink = imgList[0]
        imgId = imgList[1]
        
        end = imgLink.find('?')
        if end == -1 or end == 0:
            end = len(imgLink)
            
        if imgLink.find('preview?verifier') > 0:
            imgLink = imgLink[:imgLink.index('preview?verifier')]
        elif imgLink.find('?verifier') > 0:
            imgLink = imgLink[:imgLink.index('?verifier')]
        
        statusCode = validate_url(imgLink[:end], browser)
        
        qaInfo.errorImage[pageTitle] = qaInfo.errorImage.get(pageTitle, 0)

    
        if imgLink.find('@X@EmbeddedFile.requestUrlStub') > -1:
            statusCode = 404
        
        if statusCode > 304 or statusCode < 200:
            qaInfo.errorImage[pageTitle] += 1
        
        if altTag == '' or altTag == None:
            altTag = 'no alt tag'
            #qaInfo.errorImage[pageTitle] += 1
            error = 1
        elif altTag.find('.jpeg') > 1 or altTag.find('.jpg') > 1 or altTag.find('.png') > 1 or altTag.find('.gif') > 1:
            #qaInfo.errorImage[pageTitle] += 1
            error = 2
        else:
            error = 0
        
        if not quizpage and not pageUrl.startswith('http'):
            pageUrl = f'http://lms.griffith.edu.au/courses/{qaInfo.courseId}/pages/{pageUrl}'
            
            
        if qaInfo.imgTags.get(pageTitle, None) is None:
            qaInfo.imgTags[pageTitle] = []
        qaInfo.imgTags[pageTitle].append([pageTitle, qaInfo.courseId, pageUrl, altTag, imgLink, statusCode, error])
        
        if imgId is not None:
            qaInfo.usedFilesId.append(imgId)
        else:
            try:
                start = imgLink.index('files/') + 6
                end = imgLink[start::].index('/')
                end += start
                qaInfo.usedFilesId.append(imgLink[start:end])
            except:
                pass
        
    qaInfo.errorLinks['alttags'] = sum(qaInfo.errorImage.values())  
  
        
def linkCheck(browser, qaInfo, links, pageTitle, pageUrl, page, quizpage=False):
    for link in links:
        error = 0
        title = link[0].strip()
        
        URL = link[1]    
        
        if URL.find('preview?verifier') > 0:
            URL = URL[:URL.index('preview?verifier')]
        elif URL.find('?verifier') > 0:
            URL = URL[:URL.index('?verifier')]
        
        if URL.startswith('#'):
            URL = f'http://lms.griffith.edu.au/courses/{qaInfo.courseId}/pages/{URL}'
                         
            
        if (
            'mailto' in URL or
            'https://griffitheduau.sharepoint.com' in URL or
            'https://griffitheduau-my.sharepoint.com' in URL or
            URL.startswith('tel:') or URL.startswith('sms:') or
            URL.startswith('message?message_id')
        ):
            continue
        
        statusCode = validate_url(URL, browser)
            
        if title == '':
            error = 1
        elif title.lower() == 'click here':
            error = 2
        elif title.lower() in URL:
            error = 3
        else:
            error = 0
        

        if URL.find('@X@EmbeddedFile.requestUrlStub/') > -1:
            statusCode = 404

        
        if not quizpage and not pageUrl.startswith('http'):
            pageUrl = f'http://lms.griffith.edu.au/courses/{qaInfo.courseId}/pages/{pageUrl}'
            
        if statusCode > 399 or statusCode < 200:
            if qaInfo.links.get('Check Links', None) == None:
                qaInfo.links['Check Links'] = []
            qaInfo.links['Check Links'].append([pageTitle, qaInfo.courseId, pageUrl, title, URL, statusCode, error])
            qaInfo.errorLinks['Check Links'] = qaInfo.errorLinks.get('Check Links', 0) + 1
            qaInfo.errorLinks['total'] = qaInfo.errorLinks.get('total', 0) + 1
            #if error:
            #    qaInfo.errorLinks['Check Links'] = qaInfo.errorLinks.get('Check Links', 0) + 1
            #    qaInfo.errorLinks['total'] = qaInfo.errorLinks.get('total', 0) + 1
        elif statusCode != None:
            if qaInfo.links.get('Working Links', None) == None:
                qaInfo.links['Working Links'] = []
            qaInfo.links['Working Links'].append([pageTitle, qaInfo.courseId, pageUrl, title, URL, statusCode, error])
            #if error:
            #    qaInfo.errorLinks['Working Links'] = qaInfo.errorLinks.get('Working Links', 0) + 1
            #    qaInfo.errorLinks['total'] = qaInfo.errorLinks.get('total', 0) + 1
            #print(x.status_code)
        
        if link[2] is not None:
            qaInfo.usedFilesId.append(link[2])
        else:
            try:
                start = link[1].index('files/') + 6
                end = link[1][start::].index('?')
                end += start
                qaInfo.usedFilesId.append(link[1][start:end])
            except:
                pass
            
        """try:
            link[1].index('lms.griffith.edu.au/courses/')
            index = link[1].index('=')
            end = link[1][index:].index('&')
            end += index
            id = link[1][index+1:end]
            if qaInfo.usedFilesId.get(id, None) == None:
                qaInfo.usedFilesId[id] = []
            qaInfo.usedFilesId[id].append(page)
        except:
            pass"""