from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions

def generateUnattachedPagesHtml(myCanvas, canvasQa):
    
    
    if canvasQa.get('unattachedPages') is None:
        return ''
    
    htmlUnattachedPages = htmlUnattachedPagesGenerate(canvasQa['unattachedPages'], canvasQa['issues']['Unattached Pages']['id'], myCanvas) if len(canvasQa['unattachedPages']) > 0 else ''
    
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
                        Div([Class('columns')],
                            Div([Class('column')],
                                Table([Class('table')],
                                    Thead([],
                                        htmlUnattachedPagesAccordion(UnattachedPages, myCanvas)
                                    )
                                )
                            ), 
                        )
                    )
                )
            ),
        )    
    return html

def htmlUnattachedPagesAccordion(UnattachedPages, myCanvas):
    html = ''
    html = (html,
            P([], Em([], ["An unattached page is any page in the Canvas Course site that isn't attached to a Module.<br>"\
                    "There are a few instances where this is expected, known pages that aren't intended to be attached to modules are ignored by this check,<br>"\
                        "as a general rule anything not attached is likely not being used in the course in which can you can consider deleting such items."])),
            
            Tr([], 
                Th([], "Page Title"),
                Th([], 'Published'),
            ),
            Tbody([],
                htmlUnattachedPagesHeader(UnattachedPages, myCanvas)
            )
        )
                   
                
    return html

def htmlUnattachedPagesHeader(UnattachedPages, myCanvas):
    
    html = ''
    for id, page in UnattachedPages.items():
        html = (html,
                Tr([],
                    Td([], 
                        A([Href(page['url']), Target('_blank'), Rel('noopener noreferrer')], page['title']),
                    ),
                    Td([], page['published']),
                )
            )
    return html
