import bs4 as bs
import re
from pprint import pprint

#This module is designed to be passed a dataset of pages to process the contents of the body and title of each page. Then returns the Pages dataset with the results of the checks added to the dataset.
def checkPageBody(pages):
    usedFiles = []
    for pageId, page in pages.items():
            
        body = page.get('body', None)
        
        if body is not None and type(body) == str:
            body = body.lower()
        else:
            continue
            
        soup = bs.BeautifulSoup(body, features="html.parser")
        
        page['bbTerms'] = BBtermCheck(body, page['title'])
        page['placeholders'] = placeholderBodyCheck(body, page['title'], soup)
        page['bbhtml'] = bbhtmlCheck(soup)
        page['bbEcho'] = getBBEcho(soup)
        page['imgTags'] = getPageImgTags(soup)
        page['links'] = getPageLinks(soup)
        page['videoIframes'] = getVideoIframes(soup)
        page['fileLinks'] = getFileLinks(soup)
        
        
        usedFiles += checkForCanvasFileLink(page['links']) if page['links'] is not None else []
        usedFiles += checkForCanvasFileLink(page['imgTags']) if page['imgTags'] is not None else []
        
    return pages, usedFiles

def checkQuizBody(questions):
    usedFiles = []
    for id, question in questions.items():
        
        body = question.get('body', None)
        
        if body is not None and type(body) == str:
            body = body.lower()
        else:
            continue
            
        soup = bs.BeautifulSoup(body, features="html.parser")
        
        question['bbTerms'] = BBtermCheck(body, question['title'])
        question['placeholders'] = placeholderBodyCheck(body, question['title'], soup)
        question['bbhtml'] = bbhtmlCheck(soup)
        question['bbEcho'] = getBBEcho(soup)
        question['imgTags'] = getPageImgTags(soup)
        question['links'] = getPageLinks(soup)
        question['fileLinks'] = getFileLinks(soup)
        question['videoIframes'] = getVideoIframes(soup)
        
        
        usedFiles += checkForCanvasFileLink(question['links']) if question['links'] is not None else []
        usedFiles += checkForCanvasFileLink(question['imgTags']) if question['imgTags'] is not None else []
    
    return questions, usedFiles

#checks links if they are a canvas file link to collect the ID for a later check of the file structure       
def checkForCanvasFileLink(links):
    
    canvasUsedFilesId = []
    
    for title, link in links.items():
        if link.find('lms.griffith.edu.au'):
    
            start = link.find('files/') + 6
            end = link[start::].find('/')
            if end == -1:
                end = link[start::].find('?')
            end += start
            
            usedFileId = link[start:end]
            
            if usedFileId.isdigit() or type(usedFileId) == int:
                canvasUsedFilesId.append(int(usedFileId))
            
            
    return list(set(canvasUsedFilesId))


# checking page html for BB terms
def BBtermCheck(body, title):
    
    bbTerms = ["my marks", "collaborate", "blackboard", "bblearn", 'pass', 'pam', 'card', 
               'content', 'safeassign', 'journal', 'wiki', 'voicethread', 'fbf', 
               'feedback fruits', 'coversheet', 'cover sheet']
    
    bbTermCheck = {}
    
    for term in bbTerms:
        
        if body.find(term) > -1:  
            bbTermCheck[term] = 'Found in Page Body'
        
        if title.find(term) > -1:
            bbTermCheck['title'] = f'{term.capitalize} found in Page Title'
 
    
    return bbTermCheck if bbTermCheck != {} else None


        
def placeholderBodyCheck(body, title, soup):
    #method 1 for placeholder checking
    placeholderTerms = ['placeholder', 'unavailable', 'hidden', 'broken', 'add more', 'replace this text']
    bodyCheck = {}
    titleCheck = {}

    for term in placeholderTerms:
        
        if body.find(term) > -1:  
            bodyCheck[term] = 'Found in Page Body'
        
        if title.find(term) > -1:
            titleCheck[term] = 'Found in Page Title'

    
    #method 2 for placeholder checking - w2c tags
    for span in soup.findAll('span'):
        if span.has_attr('class'):
            if 'w2c-error' in span.get('class'):
                bodyCheck['w2c-error'] = span.get_text().strip()
    
    #method 3 for placeholder checking - word style tags
    marks = []
    for mark in soup.findAll('mark'):
        #marks.append(re.sub('<[^<]+?>', '', str(mark)))
        bodyCheck[re.sub('<[^<]+?>', '', str(mark))] = 'Author Placeholder'
        
    return bodyCheck if bodyCheck != {} else None
      
def bbhtmlCheck(soup):  
    instancesFound = []
    for span in soup.findAll('div'):
        if span.has_attr('class'):
            if len(span.get('class')) > 0:
                if span.get('class')[0] == 'vtbegenerated_div':
                    instancesFound.append(span.get_text().strip())
                    
    return instancesFound if len(instancesFound) > 0 else None
    
def getBBEcho(soup):
    instancesFound = []
    for item in soup.findAll('iframe'):
        if item.has_attr('src'):
            if item['src'].find("echo-library-BB5bb") > -1:
                instancesFound.append(item.get('title'))
   
    return instancesFound if len(instancesFound) > 0 else None
    
def getPageImgTags(soup):
    imgs = {}
    for img in soup.findAll('img'):
        if img.has_attr('src'):
            if img.has_attr('id'):
                imgs[img.get('alt')] = img.get('src')
            else:
                imgs[img.get('alt')] = img.get('src')
                
    return imgs if len(imgs) > 0 else None
         
def getFileLinks(soup):
    fileLinks = []
    for link in soup.findAll('href'):
        if link.get('href').find("https://griffitheduau.sharepoint.com") > -1 or link.get('href').find("https://griffitheduau-my.sharepoint.com") > -1:
            fileLinks[link.get_text().strip()] = link.get('href')
            
    return fileLinks if len(fileLinks) > 0 else None
      
#checking for links in page html
def getPageLinks(soup):

    links = {}
    for link in soup.findAll('a'):
        if link.has_attr('href'):
            if link.has_attr('id'):
                links[link.get_text().strip()] =  link.get('href')
            else:
                links[link.get_text().strip()] =  link.get('href')
    for link in soup.findAll('span'):
        if link.has_attr('href'):
            if link.has_attr('id'):
                links[link.get_text().strip()] =  link.get('href')
            else:
                links[link.get_text().strip()] =  link.get('href')

    return links if len(links) > 0 else None

def getVideoIframes(soup):
    iframeVideos = {}
    for item in soup.findAll('iframe'):
        if item.has_attr('src'):
            
            if item.get('src').find('youtube.com') > 1:
                host = 'YouTube'
            elif item.get('src').find('echo360.net') > 1:
                host = 'Echo360'
            elif item.get('src').find('instructuremedia.com') > 1:
                host = 'Canvas Studio'
            elif item.get('src').find('vimeo.com') > 1:
                host = 'vimeo'
            elif item.get('src').find('microsoftstream.com') > 1:
                host = 'Microsoft Stream'
            elif item.get('src').find('google.com') > 1:
                host = 'Google'
            elif item.get('src').find('griffitheduau-my.sharepoint.com') > 1:
                host = 'Griffith Sharepoint'
            elif item.get('src').find('griffith.edu.au') > 1:
                host = 'Griffith Uni'
            elif item.get('src').find('lms.griffith.edu.au') > 1:
                host = 'Canvas'
            else:
                host = 'Unknown'
            
            if iframeVideos.get(host, None) == None:
                iframeVideos[host] = {}
                
            iframeVideos[host][item.get_text().strip()] = item.get('src')
    
    return iframeVideos if len(iframeVideos) > 0 else None

