from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions

def generateUnattachedPagesHtml(myCanvas, canvasQa):
    
    
    if canvasQa.get('unattachedPages') is None:
        return ''
    
    htmlUnattachedPages = htmlUnattachedPagesGenerate(canvasQa['unattachedPages'], canvasQa['issues']['Unattached Pages']['id'], myCanvas)
    
    return htmlUnattachedPages

def htmlUnattachedPagesGenerate(UnattachedPages, id, myCanvas):
    html = (
            Article([Class('message')],
                Div([Class('message-header')],
                    P([], Span([], 'Unattached Pages'),
                        Span([Class('tag is-info ml-6')], 
                            A([Onclick(f'sectionExpand("{id}");')], 'collapse/expand')
                        ),
                        Span([Class('tag is-right is-info ml-6')], 
                            A([Href('#top'), Data_('action','collapse')], 'Back to top')
                        )
                    )
                ),
                Div([Id(id), Class('message-body is-collapsible')],
                    Div([Class('message-body-content')],
                        Div([Class('columns is-multiline is-variable is-8')],
                            Div([Class('column is-7')],
                                htmlUnattachedPagesAccordion(UnattachedPages, myCanvas)
                            ), 
                            about('Placeholders Check', getDescriptions('Placeholder'))
                        )
                    )
                )
            ),
        )    
    return html

def htmlUnattachedPagesAccordion(UnattachedPages, myCanvas):
    html = ''
    html = (html,
                Table([Class('table')],
                    Thead([],
                        #P([], Em([], ['This is a list of any Blackboard Terms used in the course and associated items'])),
                        #P([], Em([], ['These will need to be changed to reflect tools used in Canvas'])),
                        Tr([], 
                            Th([], "Page Title"),
                            Th([], 'Published'),
                            #Th([], 'Show/Hide')
                        )
                    ),
                    htmlUnattachedPagesHeader(UnattachedPages, myCanvas)
                )
            )
                
    return html

def htmlUnattachedPagesHeader(UnattachedPages, myCanvas):
    
    html = ''
    for id, page in UnattachedPages.items():
        html = (html,
            Tbody([],
                Tr([],
                    Td([], 
                        A([Href(page['url']), Target('_blank'), Rel('noopener noreferrer')], page['title']),
                    ),
                    Td([], page['published']),
                )
            )
        )
    return html
