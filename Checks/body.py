import bs4 as bs
import re
from pprint import pprint
from Checks.linkCheck import linkCheck

#This module is designed to be passed a dataset of pages to process the contents of the body and title of each page. Then returns the Pages dataset with the results of the checks added to the dataset.
def checkPageBody(pages, myCanvas):
    usedFiles = []
    for pageId, page in pages.items():
            
        body = page.get('body', None)
        
        if body is not None and type(body) == str:
            body = body.lower()
        else:
            continue
            
        soup = bs.BeautifulSoup(body, features="html.parser")
        
        page['bbTerms'] = BBtermCheck(soup, page['title'])
        page['placeholders'] = placeholderBodyCheck(soup, page['title'])
        page['bbHtml'] = bbhtmlCheck(soup)
        page['bbEcho'] = getBBEcho(soup)
        page['imgTags'] = getPageImgTags(soup, myCanvas)
        page['links'] = getPageLinks(soup, myCanvas)
        page['videoIframes'] = getVideoIframes(soup, myCanvas)
        #page['fileLinks'] = getFileLinks(soup, myCanvas)
        
        
        usedFiles += checkForCanvasFileLink(page['links']) if page['links'] is not None else []
        usedFiles += checkForCanvasFileLink(page['imgTags']) if page['imgTags'] is not None else []
        
    return pages, usedFiles

def highlightText(text, term):
    start = 0
    highlightedText = f' <mark><strong>{term}</strong></mark> '
    searchTerm = f' {term} '
    
    while start < len(text):
        match = re.search(searchTerm, text[start:])#.find(searchTerm)
        if match == None:
            return text
        end = start + match.end()
        start += match.start()
        text = text[:start] + highlightedText + text[end:]
        start = end + len(highlightedText)
        
    return text

def checkQuizBody(questions, myCanvas):
    usedFiles = []
    for id, question in questions.items():
        
        body = question.get('body', None)
        
        if body is not None and type(body) == str:
            body = body.lower()
        else:
            continue
            
        soup = bs.BeautifulSoup(body, features="html.parser")
        
        question['bbTerms'] = BBtermCheck(soup, question['title'])
        question['placeholders'] = placeholderBodyCheck(soup, question['title'])
        question['bbHtml'] = bbhtmlCheck(soup)
        question['bbEcho'] = getBBEcho(soup)
        question['imgTags'] = getPageImgTags(soup, myCanvas)
        question['links'] = getPageLinks(soup, myCanvas)
        #question['fileLinks'] = getFileLinks(soup, myCanvas)
        question['videoIframes'] = getVideoIframes(soup, myCanvas)
        
        
        usedFiles += checkForCanvasFileLink(question['links']) if question['links'] is not None else []
        usedFiles += checkForCanvasFileLink(question['imgTags']) if question['imgTags'] is not None else []
    
    return questions, usedFiles

#checks links if they are a canvas file link to collect the ID for a later check of the file structure       
def checkForCanvasFileLink(links):
    
    canvasUsedFilesId = []
    
    for title, link in links.items():
        if type(link) == dict:
            link = link.get('source', None)
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

def placeholderBodyCheck(soup, title):
    #method 1 for placeholder checking
    placeholderTerms = ['placeholder', 'unavailable', 'hidden', 'replace this text']
    placeholderCheck = {}

    for term in placeholderTerms:
        for line in soup.findAll('p'):
            if line is not None:
                if re.search(f' {term} ', line.get_text()):#line.get_text().find(term) > -1:  
                    #lineText = line.get_text().encode('ascii', 'ignore')
                    #lineText = lineText.decode().strip('[]')
                    
                    lineText = highlightText(line.get_text(), term)
                    placeholderCheck[term] = placeholderCheck.get(term, '') + lineText#'Found in Page Body'

        if title.find(term) > -1:
            if placeholderCheck.get(term, None) == None:
                placeholderCheck[term] = f'Found in Title: {title}'
            else:
                placeholderCheck[term] = f'Found in Title: {title} and\n' + placeholderCheck[term]
    
    #method 2 for placeholder checking - w2c tags
    for span in soup.findAll('span'):
        if span.has_attr('class'):
            if 'w2c-error' in span.get('class'):
                placeholderCheck['w2c-error'] = span.get_text().strip()
    
    #method 3 for placeholder checking - word style tags
    marks = []
    for mark in soup.findAll('mark'):
        #marks.append(re.sub('<[^<]+?>', '', str(mark)))
        placeholderCheck[re.sub('<[^<]+?>', '', str(mark).strip('[]'))] = 'Author Placeholder'
        
    return placeholderCheck if placeholderCheck != {} else None

# checking page html for BB terms
def BBtermCheck(soup, title):
    
    bbTerms = ["my marks", "collaborate", "blackboard", "bblearn", 'pass', 'pam', 'card', 
               'content', 'safeassign', 'journal', 'wiki', 'voicethread', 'fbf', 
               'feedback fruits', 'coversheet', 'cover sheet']
    
    bbTermCheck = {}
    for term in bbTerms:
        if type(soup) == str:
            if soup.find(term) > -1:
                bbTermCheck[term] = 'Found in Page Body'
        else:
            for line in soup.findAll('p'):
                if line is not None:
                    if re.search(f' {term} ', line.get_text()):#if line.get_text().find(term) > -1:  
                        #lineText = line.get_text().encode('ascii', 'ignore')
                        #lineText = lineText.decode()
                        lineText = highlightText(line.get_text(), term)
                        bbTermCheck[term] = bbTermCheck.get(term, '') + lineText
            
        if title.find(term) > -1:
            if bbTermCheck.get(term, None) == None:
                bbTermCheck[term] = f'Found in Title: {title}'
            else:
                bbTermCheck[term] = f'Found in Title: {title} and\n' + bbTermCheck[term]
            #bbTermCheck['title'] = f'{term.capitalize} found in Page Title'
 
    
    return bbTermCheck if bbTermCheck != {} else None
      
def bbhtmlCheck(soup):  
    instancesFound = {}
    for span in soup.findAll('div'):
        if span.has_attr('class'):
            if len(span.get('class')) > 0:
                if span.get('class')[0] == 'vtbegenerated_div':
                    instancesFound[span.get('class')[0]] = span.get_text().strip()
                    #instancesFound.append(span.get_text().strip())
                    
    return instancesFound if len(instancesFound) > 0 else None
    
def getBBEcho(soup):
    instancesFound = {}
    for item in soup.findAll('iframe'):
        if item.has_attr('src'):
            if item['src'].find("echo-library-BB5bb") > -1:
                instancesFound[item.get('title')] = item['src']
                #instancesFound.append()
   
    return instancesFound if len(instancesFound) > 0 else None
    
def getPageImgTags(soup, myCanvas):
    imgs = {}
    for img in soup.findAll('img'):
        if img.has_attr('src'):
                imgs[img.get('alt')] = {'source': img.get('src'), 'statusCode' : linkCheck(img.get('src'), myCanvas)}
                
    return imgs if len(imgs) > 0 else None
         
"""def getFileLinks(soup, myCanvas):
    fileLinks = []
    for link in soup.findAll('href'):
        if re.search("https://griffitheduau-*m*y*.sharepoint.com", link.get('href')):# link.get('href').find("https://griffitheduau.sharepoint.com") > -1 or link.get('href').find("https://griffitheduau-my.sharepoint.com") > -1:
            fileLinks[link.get_text().strip()] = link.get('href')
            
    return fileLinks if len(fileLinks) > 0 else None"""
      
#checking for links in page html
def getPageLinks(soup, myCanvas):

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

def getVideoIframes(soup, myCanvas):
    iframeVideos = {}
    for item in soup.findAll('iframe'):
        if item.has_attr('src'):
            
            if re.search('youtube.com', item['src']):#item.get('src').find('youtube.com') > 1:
                host = 'YouTube'
            elif re.search('echo360.net', item['src']):#item.get('src').find('echo360.net') > 1:
                host = 'Echo360'
            elif re.search('instructuremedia.com', item['src']):#item.get('src').find('instructuremedia.com') > 1:
                host = 'Canvas Studio'
            elif re.search('vimeo.com', item['src']):#item.get('src').find('vimeo.com') > 1:
                host = 'vimeo'
            elif re.search('microsoftstream.com', item['src']):#item.get('src').find('microsoftstream.com') > 1:
                host = 'Microsoft Stream'
            elif re.search('google.com', item['src']):#item.get('src').find('google.com') > 1:
                host = 'Google'
            elif re.search('griffitheduau-my.sharepoint.com', item['src']):#item.get('src').find('griffitheduau-my.sharepoint.com') > 1:
                host = 'Griffith Sharepoint'
            elif re.search('griffith.edu.au', item['src']):#item.get('src').find('griffith.edu.au') > 1:
                host = 'Griffith Uni'
            elif re.search('lms.griffith.edu.au', item['src']):#item.get('src').find('lms.griffith.edu.au') > 1:
                host = 'Canvas'
            else:
                host = 'Unknown'
            
            if iframeVideos.get(host, None) == None:
                iframeVideos[host] = {}
                
            iframeVideos[host][item.get_text().strip()] = item.get('src')
    
    return iframeVideos if len(iframeVideos) > 0 else None

