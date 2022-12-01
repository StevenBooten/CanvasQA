from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style as InlineStyle
from Checks.linkCheck import linkCheck
from htmlgeneration.extraHtmlFunctions import about, errorUnpublishedItems
from lib.InfoPacks import getDescriptions

def generateModulesHtml(myCanvas, canvasQa):
    
    
    if canvasQa.get('modules') is None:
        return ''
    
    htmlFileStructure = moduleAccordian(canvasQa, canvasQa['issues']['Modules']['id']) if len(canvasQa['modules']) > 0 else ''
    
    return htmlFileStructure
    
def moduleAccordian(canvasQa, id):
    html = (                    
        Article([Class('message')],
            Div([Class('message-header')],
                P([], Span([], 'Modules Check'), errorUnpublishedItems(canvasQa['issues']['Modules']['unpublishedModules'], 'modules'), errorUnpublishedItems(canvasQa['issues']['Modules']['unpublishedItems'], 'items'),
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
                            Table([Class('table')],
                                Thead([],
                                    P([], Em([Class('is-multiline')], ['In Canvas, Modules are the primary tool for structuring student learning activities. <br>\
                                                                        The ability for students to easily find learning activities is the most significant predictor of student self-efficacy<br> \
                                                                        and motivation (Crews et al, 2017). The naming and availability of modules and module items can help. The UDL for Module Design page provides more advice.'])), 
                                    Tr([], 
                                        Th([], 'Position'),
                                        Th([], 'Module Name'),
                                        Th([], '# of Items'),
                                        Th([], 'Published'),  
                                        Th([], 'Show/Hide')
                                    )
                                ), 
                                Tbody([],
                                    moduleHtml(canvasQa['modules'])
                                )
                            )
                        ), 
                    )
                )
            )  
        )    
    )                     
    
    return html

def moduleHtml(canvasQa):
    
    html = ''
    for id, module in canvasQa.items():
        if type(module) == int:
            continue
        html = (html, 
                Tr([],
                    Td([], module['position']),
                    Td([], 
                        A([Href(module['url']), Target('_blank'), Rel('noopener noreferrer')], module['title']), errorUnpublishedItems(module['unpublishedItems'], 'item') if module.get('unpublishedItems', 0) > 0 else '',
                    ),
                    Td([], str(module['itemsCount'])),   
                        
                    Td([], module['published']) if module['published'] == 'Yes' else Td([Class('is-warning has-tooltip-left has-tooltip-multiline'), Data_('tooltip', 'Students are unable to see unpublished Modules, Publish if students need to see it.')], 'No'),
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
                                        Tbody([],
                                            moduleItems(module['items'])
                                        )
                                    )
                                )
                            )
                        )
                    ) if module['itemsCount'] > 0 else '',
                )
            )
    return html

def moduleItems(items):
    html = ''
    for item in items:
        html = (html,
                Tr([],
                    Td([], item['position']),
                    Td([], item['indent']),
                    Td([], 
                        A([Href(item['url']), Target('_blank'), Rel('noopener noreferrer')], item['title'])
                    ),
                    Td([], item['type']),
                    Td([], item['published']) if item['published'] == 'Yes' else Td([Class('is-warning has-tooltip-left has-tooltip-multiline'), Data_('tooltip', 'Students are unable to see unpublished items, Publish if students need to see it.')], 'No')
                )   
            )
                
    return html