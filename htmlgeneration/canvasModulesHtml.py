from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style as InlineStyle
from Checks.linkCheck import linkCheck
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions

def generateModulesHtml(myCanvas, canvasQa):
    
    
    if canvasQa.get('modules') is None:
        return ''
    
    htmlFileStructure = moduleAccordian(canvasQa, canvasQa['issues']['Modules']['id'])
    
    return htmlFileStructure
    
def moduleAccordian(canvasQa, id):
    html = (                    
        Article([Class('message')],
            Div([Class('message-header')],
                P([], Span([], 'Modules Check'),
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
                    Div([Class('columns is-multiline is-variable is-8')],
                        Div([Class('column is-7 is-narrow')],
                            Table([Class('table')],
                                Thead([],
                                    P([], Em([], ['This is a list of modules in the course and associated items'])), 
                                    P([], Em([], ['Please Check that Module and Item names are correct, consistent, logical, and has been published.'])),
                                    Tr([], 
                                        #Th([], 'ID'),
                                        Th([], 'Position'),
                                        Th([], 'Module Name'),
                                        Th([], '# of Items'),
                                        Th([], 'Published'),  
                                        Th([], 'Show/Hide')
                                    )
                                ),
                                moduleHtml(canvasQa['modules'])
                            )
                        ), about('Modules Check', getDescriptions('Module'))
                    )
                )
            )  
        )    
    )                     
    
    return html

def moduleHtml(canvasQa):
    
    html = ''
    for id, module in canvasQa.items():
        html = (html, 
            Tbody([], 
                Tr([],
                    #Td([], module['ID']),
                    Td([], module['position']),
                    Td([], 
                        A([Href(module['url']), Target('_blank'), Rel('noopener noreferrer')], module['title']),
                    ),
                    Td([], str(module['itemsCount'])),   
                        
                    Td([], module['published']),
                    Td([],
                        Span([Class('tag is-info is-size-7')],
                            A([Href(f'#collapsible-items-{id}'), Data_('action','collapse')], 'Show Module Contents')
                            
                        )
                    ),
                    Tr([Id(f'collapsible-items-{id}'), Class('is-collapsible')],
                        Td([Colspan('6')],
                            Div([],
                                Div([Id(f'collapsible-items-{id}'), Class('is-collapsible')],
                                    Table([Class('table is-fullwidth is-bordered is-striped is-size-7')],
                                        Thead([],
                                            Tr([], 
                                                Th([], 'Position'),
                                                Th([], 'Indent'),
                                                Th([], 'Item Name'),
                                                Th([], 'Type'),
                                                Th([], 'Published')                                                     
                                            )
                                        ),
                                        moduleItems(module['items'])
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    return html

def moduleItems(items):
    html = ''
    for item in items:
        html = (html,
                    Tbody([],
                        Tr([],
                            Td([], item['position']),
                            Td([], item['indent']),
                            Td([], 
                                A([Href(item['url']), Target('_blank'), Rel('noopener noreferrer')], item['title']),
                            ),
                            Td([], item['type']),
                            Td([], item['published'])
                        )   
                    )
                )
    return html