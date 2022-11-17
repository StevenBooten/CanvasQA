from canvasapi import Canvas
import re

#- Purpose of this module is  to cycle through every module in a course and pulls all necessary information
#- Any manipulation of the data is done elsewhere
def collectCourseModules(myCanvas):
    
    moduleItem = {}
    
    moduleQa = {}
    usedFiles = []
    
    for module in myCanvas.getModules():
        moduleItemList = [] 
        for item in myCanvas.getModuleItems(module.id):
            #- Clears the dictionary for each module item
            moduleItem = {}
            
            #- Adds the module item's information a the dictionary
            moduleItem['position'] = str(item.position)
            moduleItem['indent'] = str(item.indent)
            moduleItem['title'] = str(item.title)
            moduleItem['type'] = str(item.type)
            moduleItem['id'] = item.id
            #- Not all module items have a relevant URL ie subtitles
            try:
                moduleItem['url'] = str(item.html_url)
            except:
                moduleItem['url'] = ''
        
            #- Publishes returns a boolean value, so it needs to be converted to a string
            if item.published:
                moduleItem['published'] = 'Yes'
            else:
                moduleItem['published'] = 'No' 
                
            if item.type == 'File':
                usedFiles.append(item.content_id)

            moduleItemList.append(moduleItem)
            
        #- Collects all module information including all the module items.      
        moduleQa[module.id] = {}
        moduleQa[module.id]['id'] = str(module.id)
        moduleQa[module.id]['position'] = str(module.position)
        moduleQa[module.id]['title'] = str(module.name)
        moduleQa[module.id]['itemsCount'] = module.items_count
        moduleQa[module.id]['url'] = str(f'http://lms.griffith.edu.au/courses/{myCanvas.courseId}/modules/#module_{module.id}')
        moduleQa[module.id]['items'] = moduleItemList
        #- Publishes returns a boolean value, so it needs to be converted to a string
        if module.published:
            moduleQa[module.id]['published'] = 'Yes'
        else:
            moduleQa[module.id]['published'] = 'No'
            
    return moduleQa, usedFiles

#- finds all pages in a course and checks them against the module items dataset to attain
#- whether they are linked to a module
def unattachedPages(myCanvas, moduleQa, pages):
    
    ignoredPages = ['canvas-collections-configuration']
    pagesInModules = []
    
    for key, value in moduleQa.items():
        for item in value['items']:
            if item['type'] == 'Page':
                pagesInModules.append(item['id'])
                
    unattachedPages = {}
    
    for key, page in pages.items():
        if key in pagesInModules or page['title'] in ignoredPages:
            continue
        
        unattachedPages['title'] = page['title']
        unattachedPages['id'] = key
        #- page url only holds "my-page-title" so creating a valid URL to the actual page in the course.
        unattachedPages['url'] = page['url']
        unattachedPages['published'] = page['published']
 
    
    return unattachedPages


def collectCoursePages(myCanvas):
    
    myPages = {}
    
    for page in myCanvas.getPages():
        
        myPages[page.page_id] = {}
        myPages[page.page_id]['title'] = str(page.title)
        #- page url only holds "my-page-title" so creating a valid URL to the actual page in the course.
        myPages[page.page_id]['url'] = f'http://lms.griffith.edu.au/courses/{myCanvas.courseId}/pages/{page.url}'
        myPages[page.page_id]['body'] = myCanvas.getPage(page.page_id).body
        myPages[page.page_id]['links'] = []
        
        #- Publishes returns a boolean value, so it needs to be converted to a string
        if page.published:
            myPages[page.page_id]['published'] = 'Yes'
        else:
            myPages[page.page_id]['published'] = 'No' 
        
    return myPages
            