from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style as InlineStyle
from Checks.linkCheck import linkCheck
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions
from htmlgeneration.extraHtmlFunctions import fileStructureFolderError


def generateFileStructureHtml(myCanvas, canvasQa):
    canvasQa['issues']['File Structure']['id'] = "collapsible-filestructure-check"
    if canvasQa.get('files') is None:
        return ''
    htmlFileStructure = fileStructureAccordian(canvasQa, canvasQa['issues']['File Structure']['id'])
    
    return htmlFileStructure
    
def fileStructureAccordian(canvasQa, id):
    
    html = ''
    html = (   
        Article([Class('message')],
            Div([Class('message-header')],
                P([], Span([], 'File Structure'), #accordionError(qaInfo.errorFiles['total']),
                    Span([Class('tag is-info ml-6')], 
                        A([Onclick(f'sectionExpand("{id}");')], 'collapse/expand')
                    ),
                    Span([Class('tag is-right is-info ml-6')], 
                        A([Href(f'#top'), Data_('action','collapse')], 'Back to top')
                    )
                )
            ),
            Div([Id(id), Class('message-body is-collapsible')],
                Div([Class('message-body-content')],
                    Div([Class('columns is-multiline')],
                        Div([Class('column is-8 is-narrow toggle')],
                            Div([Class('table-container')],
                                Table([Class('table')],
                                    Thead([],
                                            P([], Em([], ['This is a complete breakdown of the file structure in the course.'])), 
                                            P([], Em([], ['Please ensure the structure is logical consistent within the course.'])),
                                        Tr([], 
                                            Th([], 'Folder'),
                                            Th([], '# of files'),
                                            Th([], 'Show/Hide')
                                        )
                                    ),
                                    fileStructureHtml(canvasQa['files'])
                                )
                            )
                        ),about('File Structure Check', getDescriptions('File Structure'))
                    )
                )
            )  
        )    
    )                     
    
    return html

def fileStructureHtml(files):
    
    html = ''
    tabsize = 5
    maxFolderSize = 30
    overallHeadingSize = 100
    for folder, items in sorted(files.items()):
        if folder == '/':
            tabstring = ''
            count = 0
        else:
            count = folder.count('/')
            tabstring = '&nbsp;'*(count*tabsize)
        if count > 1:
            folders = folder.split('/')
            title = ''
            space = (overallHeadingSize - (len(folders[-1][:maxFolderSize]) + (count*tabsize)))//len(folders)
            for folder in folders[:-1]:
                title += folder[:space] + '/'
            title += folders[-1][:maxFolderSize]
        else:
            title = folder
        html = (html,
            Tbody([],
                Tr([],
                    Td([], tabstring,
                        A([Href(items['url']), Target('_blank'), Rel('noopener noreferrer')], title), fileStructureFolderError(items['files']), 
                    ),
                    Td([], str(items['fileCount'])),
                    Td([],
                        Span([Class('tag is-info is-size-7')],
                            A([Href(f'#collapsible-items-{title}-img'), Data_('action','collapse')], 'Show Folder Contents') if len(items['files']) > 0 else A([Data_('action','collapse')], 'No Folder Contents')
                            
                        )
                    ),
                    Tr([Id(f'collapsible-items-{title}-img'), Class('is-collapsible')],
                        Td([Colspan('6')],
                            Div([],
                                Div([Id(f'collapsible-items-{title}-img'), Class('is-collapsible')],
                                    Table([Class('table is-fullwidth is-bordered is-striped is-size-7')],
                                        Thead([],
                                            Tr([], 
                                                Th([], 'File Name'),
                                                Th([], 'Used in Course'),
                                                Th([], 'Copies Found')
                                                #Th([], 'Image Link URL')                                                   
                                            )
                                        ),
                                        fileStructureItems(items['files']) 
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        
    return html

def fileStructureItems(items):
    html = ''
    for item in items:
        
        html = (html, #Html([], html,
                Tbody([],
                    Tr([],
                        Td([],
                        A([Href(item['url']), Target('_blank'), Rel('noopener noreferrer')], item['name']), #errorUnusedFiles(item[6]), errorDuplicateFiles(item[5])
                        ),
                        Td([], 'Yes' if item['used'] == True else 'No'),
                        Td([], str(item['count'])),
                    )   
                )
            )
    return html