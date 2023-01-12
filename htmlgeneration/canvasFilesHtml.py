from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style as InlineStyle
from Checks.linkCheck import linkCheck
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions
from htmlgeneration.extraHtmlFunctions import fileStructureFolderError, errorFileDuplicates, fileStructureSummary


def generateFileStructureHtml(myCanvas, canvasQa):
    
    if canvasQa.get('files') is None:
        return ''
    htmlFileStructure = fileStructureAccordian(canvasQa, canvasQa['issues']['File Structure']['id']) if len(canvasQa['files']) > 0 else ''
    
    return htmlFileStructure
    
def fileStructureAccordian(canvasQa, id):
    
    html = ''
    html = (   
        Article([Class('message')],
            Div([Class('message-header')],
                P([], Span([], 'File Structure'), fileStructureSummary(canvasQa['issues']['File Structure']),
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
                    Div([Class('columns')],
                        Div([Class('column')],
                            Div([Class('table-container')],
                                Table([Class('table')],
                                    Thead([],
                                            P([], Em([], ['This is a complete breakdown of the file structure in the course. Please ensure the structure is logical consistent within the course.<br>'\
                                                            'There is also an idication if the file has been used within the course and whether there are duplicate version of a file - <br>'\
                                                            'this can only tell you if there are multiple files with the same filename, not if there are multiple different version of the same file.'])), 
                                        Tr([], 
                                            Th([], 'Folder'),
                                            Th([], '# of files'),
                                            Th([], 'Show/Hide')
                                        )
                                    ),
                                    Tbody([],
                                        fileStructureHtml(canvasQa)
                                    )
                                )
                            )
                        ),
                    )
                )
            )  
        )    
    )                     
    
    return html

def fileStructureHtml(canvasQa):
    
    html = ''
    tabsize = 5
    maxFolderSize = 30
    overallHeadingSize = 100
    for folder, items in sorted(canvasQa['files'].items()):
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
                Tr([],
                    Td([], tabstring,
                        A([Href(items['url']), Target('_blank'), Rel('noopener noreferrer')], title), fileStructureFolderError(items['files']), 
                    ),
                    Td([], str(items['fileCount'])),
                    Td([],
                        Span([Class('tag is-info is-size-7')],
                            A([Href(f'#collapsible-items-{title}-img'), Data_('action','collapse')], 'Show Folder Contents')) if len(items['files']) > 0 else Span([Class('tag is-primary is-size-7')], 'No Files in Folder')
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
                                            )
                                        ),
                                        Tbody([],
                                            fileStructureItems(items['files'], canvasQa) 
                                        )
                                    )
                                )
                            )
                        )
                    ) if items['fileCount'] > 0 else ''
                )
            )
        
    return html

def fileStructureItems(items, canvasQa):
    html = ''
    for item in items:
        
        html = (html,
                Tr([],
                    Td([],
                    A([Href(item['url']), Target('_blank'), Rel('noopener noreferrer')], item['name']),
                    ),
                    Td([], 'Yes') if item['used'] == True else Td([Class('is-warning'), Data_('tooltip', "If a file is not being used anymore you may want to delete it.")], 'No'),
                    Td([], str(item['count'])) if item['count'] == 1 else Td([Class('is-info')], errorFileDuplicates(item['name'], canvasQa['fileReference'])),
                )   
            )
    return html