from canvasapi import Canvas
import re
from pprint import pprint

IGNORED_PAGES = ['Canvas Collections Configuration']

#- Purpose of this module is  to cycle through every module in a course and pulls all necessary information
#- Any manipulation of the data is done elsewhere
def collectCourseModules(myCanvas, canvasQa):
    
    moduleItem = {}
    
    canvasQa['modules'] = {}
    canvasQa['issues']['Modules']['unpublishedModules'] = 0
    canvasQa['issues']['Modules']['unpublishedItems'] = 0
    usedFiles = []
    
    
    for module in myCanvas.getModules():
        moduleItemList = [] 
        unpublishedCountItems = 0
        for item in myCanvas.getModuleItems(module.id):
            #- Clears the dictionary for each module item
            moduleItem = {}
           
            #- Adds the module item's information a the dictionary
            moduleItem['position'] = str(item.position)
            moduleItem['indent'] = str(item.indent)
            moduleItem['title'] = str(item.title)
            moduleItem['type'] = str(item.type)
            try:
                moduleItem['id'] = item.content_id
            except Exception as e:
                moduleItem['id'] = item.id
            #- Not all module items have a relevant URL ie subtitles
            if item.type == 'Page':
                moduleItem['url'] = f'http://lms.griffith.edu.au/courses/{myCanvas.courseId}/pages/{item.page_url}'
            else:
                try:
                    moduleItem['url'] = str(item.html_url)
                except:
                    moduleItem['url'] = ''
        
            #- Publishes returns a boolean value, so it needs to be converted to a string
            if item.published:
                moduleItem['published'] = 'Yes'
            elif item.type.lower() == 'subheader':
                moduleItem['published'] = 'Yes'
            else:
                moduleItem['published'] = 'No' 
                unpublishedCountItems += 1
                canvasQa['issues']['Modules']['count'] += 1
                canvasQa['issues']['Modules']['unpublishedItems'] += 1
                
                
            if item.type == 'File':
                usedFiles.append(item.content_id)

            moduleItemList.append(moduleItem)
            
        #- Collects all module information including all the module items.      
        canvasQa['modules'][module.id] = {}
        canvasQa['modules'][module.id]['id'] = str(module.id)
        canvasQa['modules'][module.id]['position'] = str(module.position)
        canvasQa['modules'][module.id]['title'] = str(module.name)
        canvasQa['modules'][module.id]['itemsCount'] = module.items_count
        canvasQa['modules'][module.id]['url'] = str(f'http://lms.griffith.edu.au/courses/{myCanvas.courseId}/modules/#module_{module.id}')
        canvasQa['modules'][module.id]['items'] = moduleItemList
        canvasQa['modules'][module.id]['unpublishedItems'] = unpublishedCountItems
        canvasQa['modules'][module.id]['unlockedAt'] = module.unlock_at
        canvasQa['modules'][module.id]['sequential'] = module.require_sequential_progress
        canvasQa['modules'][module.id]['preReq'] = module.prerequisite_module_ids
        
        
        #- Publishes returns a boolean value, so it needs to be converted to a string
        if module.published:
            canvasQa['modules'][module.id]['published'] = 'Yes'
        else:
            canvasQa['modules'][module.id]['published'] = 'No'
            canvasQa['issues']['Modules']['count'] += 1
            canvasQa['issues']['Modules']['unpublishedModules'] += 1
            
    return usedFiles

#- finds all pages in a course and checks them against the module items dataset to attain
#- whether they are linked to a module
def unattachedPages(myCanvas, canvasQa):
    
    ignoredPages = ['canvas collections configuration', 'home page', 'home page - banner', 'learning journey', 'assessment overview', 'learning journey 2', 'teaching staff']
    pagesInModules = []
    
    for key, value in canvasQa['modules'].items():
        for item in value.get('items', []):
            if item['type'] == 'Page':
                pagesInModules.append(item['url'])
                
               
    unattachedPages = {}
    
    
    for key, page in canvasQa['pages'].items():
        if page['url'] in pagesInModules or page['title'].lower() in ignoredPages:
            continue
        unattachedPages[key] = {}
        unattachedPages[key]['title'] = page['title']
        
        #- page url only holds "my-page-title" so creating a valid URL to the actual page in the course.
        unattachedPages[key]['url'] = page['url']
        unattachedPages[key]['published'] = page['published']
        
    canvasQa['issues']['Unattached Pages']['count'] = len(unattachedPages)
    
    return unattachedPages


def collectCoursePages(myCanvas):
    
    myPages = {}
    
    for page in myCanvas.getPages():
        
        if page.title in IGNORED_PAGES:
            continue
        
        myPages[page.page_id] = {}
        myPages[page.page_id]['title'] = str(page.title)
        #- page url only holds "my-page-title" so creating a valid URL to the actual page in the course.
        myPages[page.page_id]['url'] = f'http://lms.griffith.edu.au/courses/{myCanvas.courseId}/pages/{page.url}'
        myPages[page.page_id]['body'] = myCanvas.getPage(page.page_id).body
        myPages[page.page_id]['links'] = {}
        myPages[page.page_id]['frontPage'] = page.front_page
        
        #- Publishes returns a boolean value, so it needs to be converted to a string
        if page.published:
            myPages[page.page_id]['published'] = 'Yes'
        else:
            myPages[page.page_id]['published'] = 'No' 
        
    return myPages
            