from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions
from htmlgeneration.extraHtmlFunctions import statusCodeInfo, errorBrokenLink

def generateEmbeddedContentHtml(myCanvas, canvasQa):
    
    embeddedContentData = {}
    embeddedContentData['Page'] = {}
    embeddedContentData['Quiz'] = {}
    
    for pageId, pageData in canvasQa['pages'].items():
        if pageData.get('embeddedContent') == None:
            continue
        embeddedContentData['Page'][pageId] = {}
        embeddedContentData['Page'][pageId]['title'] = pageData['title']
        embeddedContentData['Page'][pageId]['url'] = pageData['url']
        embeddedContentData['Page'][pageId]['embeddedContent'] = pageData['embeddedContent']
        
    for assessmentGroupId, assessmentGroupData in canvasQa['assignments'].items():
        for assessmentId, assessmentData in assessmentGroupData['assignments'].items():
            if 'online_quiz' not in assessmentData['submissionTypes']:
                continue
            for questionId, quizData in assessmentData['quiz'].items():
                if quizData['embeddedContent'] == None:
                    continue
                embeddedContentData['Quiz'][assessmentId] = {}
                embeddedContentData['Quiz'][assessmentId]['title'] = assessmentData['title']
                embeddedContentData['Quiz'][assessmentId]['url'] = assessmentData['url']
                embeddedContentData['Quiz'][assessmentId]['embeddedContent'] = quizData['embeddedContent']
                
    if embeddedContentData.get('Page') is None and embeddedContentData.get('Quiz') is None:
        return ''
    htmlembeddedContent = htmlEmbeddedContentGenerate(embeddedContentData, canvasQa['issues']['Embedded Content']['id'], myCanvas) 
    
    return htmlembeddedContent

def htmlEmbeddedContentGenerate(embeddedContentData, id, myCanvas):
    html = (
            Article([Class('message')],
                Div([Class('message-header')],
                    P([], Span([], 'Embedded Content'),
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
                                htmlEmbeddedContentAccordian(embeddedContentData, myCanvas)
                            ), 
                        )
                    )
                )
            ),
        )    
    return html

def htmlEmbeddedContentAccordian(embeddedContentData, myCanvas):
    html = ''
    for key, values in embeddedContentData.items():
        if len(values) == 0:
            continue
        html = (html,
                    Table([Class('table')],
                        Thead([],
                               P([], Em([], ['This is a complete list of every piece of embedded content in the Canvas course site.<br>'\
                                            'This is broken down by Page, each item has a link check run and show you the link and the host.']
                               )),
                                Tr([], 
                                    Th([], f'{key} Name'),
                                    Th([], '# of Items'),
                                    Th([], 'Show/Hide')
                                )
                        ),
                        Tbody([],
                            htmlEmbeddedContentHeader(values, myCanvas)
                        )
                    )
                )
                
    return html

def htmlEmbeddedContentHeader(values, myCanvas):
    
    html = ''
    statusCodeErrors = []
    for id, info in sorted(values.items()):
        sumItems = len(info['embeddedContent']) if info['embeddedContent'] is not None else 0
        if sumItems == 0:
            continue
        for altTag, source in info['embeddedContent'].items():
            if 200 > source['statusCode'] or source['statusCode'] >= 300:
                statusCodeErrors.append(source['statusCode'])
        statusCodeErrors = list(set(statusCodeErrors))
        html = (html,
                Tr([],
                    Td([], 
                        A([Href(info['url']), Target('_blank'), Rel('noopener noreferrer')], info['title']), errorBrokenLink(statusCodeErrors) if len(statusCodeErrors) > 0 else ''
                    ),
                    Td([], str(sumItems)),
                    Td([],
                        Span([Class('tag is-info is-size-7')],
                            A([Href(f'#collapsible-items-placeholder-{id}'), Data_('action','collapse')], 'Show Items')
                        )
                    ),
                    Tr([Id(f'collapsible-items-placeheolder-{id}'), Class('is-collapsible')],
                        Td([Colspan('6')],
                            Div([],
                                Div([Id(f'collapsible-items-placeholder-{id}'), Class('is-collapsible')],
                                    Table([Class('table is-fullwidth is-bordered is-striped is-size-7')],
                                        Thead([],
                                            Tr([], 
                                                Th([], 'Status Code'),
                                                Th([], 'Host'),
                                                Th([], 'Source URL'),                                          
                                            )
                                        ),
                                        Tbody([],
                                            htmlEmbeddedContentItems(info, myCanvas)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
    return html

def htmlEmbeddedContentItems(info, myCanvas):
    html = ''
    for host, source in sorted(info['embeddedContent'].items(), key=lambda x: x[1]['statusCode']):
        html = (html,
            Tr([],
                Td([], 
                    statusCodeInfo(source['statusCode'])
                ),
                Td([], host),
                Td([], 
                    A([Href(source['source']), Target('_blank'), Rel('noopener noreferrer')], source['source']))
                ),
            )   
    return html