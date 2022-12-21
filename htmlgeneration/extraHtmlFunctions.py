from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style as InlineStyle
from Checks.linkCheck import linkCheck
from lib.InfoPacks import getStatusCode

def about(title, description):
    html = (
        Div([Class('column is-1')]
        ),
            Div([Class('column')],
                Article([Class('message is-primary')],
                    Div([Class('message-header')],
                        P([], title,)
                        ),
                    Div([Class('message-body')],
                        P([],'Description of checks to be made:'),
                            Ol([],
                                [Li([], x) for x in description],
                            )
                        )  
                    )
                )
            )
    return html


##############################################################################################################################
#                           error checks
#
# This is where all the functions that create warning or success messages are kept for various areas of the report.
##############################################################################################################################

#returns warnning if there is error in the accordion otherwise an okay tooltip.
def accordionError(count):
    if count > 0:
        html = (
        Span([Class('tag is-warning ml-2 has-tooltip-multiline has-tooltip-right'), Data_('tooltip', 'Automated Warnings to double check')], f'{count} Warnings',
                                Span([Class('icon is-small ml-4')], 
                                    I([Class("fas fa-exclamation-triangle")])
                                )
                            )
        )
    else:
        html = (
            Span([Class('tag is-success has-tooltip-multiline has-tooltip-right'), Data_('tooltip', 'No Automated Warnings')],
                Span([Class('icon is-small')], 
                    I([Class("fas fa-thumbs-up")])
                )
            )
        )
        
    return html

#returns error text if there is a number of errors in a sub folder otherwise an okay tooltip
def errorFolder(count):
    if count > 0:
        html = (
        Span([Class('tag is-warning has-tooltip-multiline has-tooltip-right'), Data_('tooltip', 'Contains errors that need to be checked')],
                Span([Class('icon is-small')], 
                    I([Class("fas fa-exclamation-triangle")])
                )
            )
        )
    else:
        html = (
            Span([Class('tag is-success has-tooltip-multiline has-tooltip-right'), Data_('tooltip', 'This folder contains no automated errors')],
                Span([Class('icon is-small')], 
                    I([Class("fas fa-thumbs-up")])
                )
            )
        )
        
    return html


#returns error for unused files
def errorUnusedFiles(count):
    if count > 0:
        html = (
            Span([Class('tag is-warning has-tooltip-multiline has-tooltip-right'), Data_('tooltip', 'This file has not been linked inside the course.')],
                    Span([Class('icon is-small')], 
                        I([Class("fas fa-exclamation-triangle")])
                    )
                )
            )
    else:
        html = ''
    return html
    
#returns error based on duplicate file count.  
def errorDuplicateFiles(count):
    if count > 0:
        html = (
            Span([Class('tag is-warning has-tooltip-multiline has-tooltip-right'), Data_('tooltip', 'This file has duplicate copies inside the file structure.')],
                    Span([Class('icon is-small')], 
                        I([Class("fas fa-exclamation-triangle")])
                    )
                )
            )
    else:
        html = ''
    return html

#returns error if there is only 1 item in a module.    
def errorModuleItems(item, error):
    html = str(item)
    if error:
        html = (html, #Html([], 
            Span([Class("tag is-warning has-tooltip-right has-tooltip-multiline has-tooltip-right"), Data_('tooltip', "Perhaps some warning about how modules with 1 item probably indicate a need to re-design the structure of modules")],
                Span([Class('icon is-small')],
                    I([Class('fas fa-exclamation-triangle')]
                    )
                )
            )
        )
    return html

#returns an error if assessment groups weight dont equal 100%
def errorAssessments(item, noAssignments):
    html = ''
    if item != 100:
        html = ( html, 
            Span([Class("tag is-warning ml-2 has-tooltip-right has-tooltip-multiline has-tooltip-right"), Data_('tooltip', "Total group weight is not 100")], 'Warning',
                Span([Class('icon is-small ml-4')],
                    I([Class('fas fa-exclamation-triangle')]
                    )
                )
            )
        )
        
    if noAssignments:
        html = (html, 
            Span([Class("tag is-danger has-tooltip-right has-tooltip-multiline has-tooltip-right"), Data_('tooltip', "No Assignments")], 'Warning No Assignments',
                Span([Class('icon is-small')],
                    I([Class('fas fa-exclamation-triangle')]
                    )
                )
            )
        )
        
    if html == '':
        html = (
            Span([Class('tag is-success has-tooltip-multiline has-tooltip-right'), Data_('tooltip', 'This folder contains no automated errors')],
                Span([Class('icon is-small')], 
                    I([Class("fas fa-thumbs-up")])
                )
            )
        )
    return html


   
 
#returns appropriate html for the title error passed in       
def checkLinkTitle(title, error):
    if error == 1:
        html = ( title,
                    Span([Class("tag is-warning has-tooltip-right has-tooltip-multiline has-tooltip-right"), Data_('tooltip', "Title is blank and therefore is likely broken HTML inside of the page.")],
                        Span([Class('icon is-small')],
                            I([Class('fas fa-exclamation-triangle')]
                            )
                        )
                    )
                )
            
    elif error == 2:
        html = ( title,
            Span([Class("tag is-warning has-tooltip-right has-tooltip-multiline has-tooltip-right"), Data_('tooltip', "A meaningful title helps students understand intent, esepcially thouse with screen readers.")],
                Span([Class('icon is-small')],
                    I([Class('fas fa-exclamation-triangle')]
                    )
                )
            )
        )
    elif error == 3:
        html = ( title,
            Span([Class("tag is-warning has-tooltip-right has-tooltip-multiline has-tooltip-right"), Data_('tooltip', "A meaningful title helps students understand intent, esepcially thouse with screen readers.")],
                Span([Class('icon is-small')],
                    I([Class('fas fa-exclamation-triangle')]
                    )
                )
            )
        )
    else:
        html = title
    return html
#**********************************************************************************************************************
#   Currently in Use
#**********************************************************************************************************************
def longName(name, length = 80):
    if len(name) < length:
        return name
    x = len(name) // length
    newName = ''
    start = 0
    for x in range(0, x):
        end = start + length
        newName += f'{name[start:end]}<br>'
        start = end
    newName += name[start:]
        
    return newName

#returns status code info from the dictionary based on the reponse code passed in.
def statusCodeInfo(statusCode):
    if statusCode >= 200 and statusCode < 300:
        html = (
                Span([Class("tag is-success has-tooltip-right has-tooltip-multiline width=30rem"), Data_('tooltip', getStatusCode(str(statusCode)))],[str(statusCode)]  
                )
        )
    elif statusCode > 200 and statusCode < 400:
        html = (
                Span([Class("tag is-warning has-tooltip-right has-tooltip-multiline"), Data_('tooltip', getStatusCode(str(statusCode)))],[str(statusCode)]  
                )
        )
    else:
        html = (
                Span([Class("tag is-danger has-tooltip-right has-tooltip-multiline"), Data_('tooltip', getStatusCode(str(statusCode)))],[str(statusCode)]  
                )
        )
    return html

#adds a warning to the folder title of an accordion if there are any issues with files within that folder
def fileStructureFolderError(files):
    unusedHtml = ''
    duplicateHtml = ''
    
    
    for item in files:
        if item['used'] == False:
            unusedHtml = ('&nbsp;',
                Span([Class('tag is-warning has-tooltip-multiline has-tooltip-right'), Data_('tooltip', "There are file(s) in this folder that are not linked in the course.")],
                    'Unused Files',
                    #Span([Class('icon is-small')], 
                    #    I([Class("fas fa-exclamation-triangle")])
                    #)
                )
            ),
        if item['count'] > 1:
            duplicateHtml = ('&nbsp;',
                Span([Class('tag is-info has-tooltip-multiline has-tooltip-right'), Data_('tooltip', 'This contains a file which has a duplicate copy in the file structure.')],
                    'Duplicate Files',
                    #Span([Class('icon is-small')], 
                    #    I([Class("fas fa-exclamation-triangle")])
                    #)
                )
            ),
    
    return unusedHtml, duplicateHtml

def errorUnpublishedItems(count, title):
    if count > 0:
        html = ( 
                Span([Class("tag is-warning has-tooltip-multiline has-tooltip-right"), Data_('tooltip', f"There are unpublished {title} in this folder, Students are unable to see unpublished {title}. Publish if students need to see it.")], f'{count} Unpublished {title.capitalize()}',)
                )
    
    return html if count > 0 else ""
        
# returns warrning html if there is an error with the alt tag
def errorBrokenLink(statusCodes):
    html = ('&nbsp;',
        Span([Class("tag has-tooltip-right has-tooltip-multiline has-tooltip-right"), Data_('tooltip',"There are broken links in this page")],
             'Broken Link(s) found: ', [statusCodeInfo(code) for code in statusCodes],
        )
    )
    
    return html 

def errorFileDuplicates(fileName, fileref):
    html = ''
    for count, values in enumerate(fileref[fileName]['folders']):
        for folder, url in values.items():
            html = (html, A([Class('has-tooltip-left'), Href(f"url"), Data_('tooltip', f"A copy of this file is in folder: {folder}")], count+1),
            "&nbsp;&nbsp;" if count < len(fileref[fileName]['folders']) else ''
            )
    
    
    return html