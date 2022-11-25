from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions
from htmlgeneration.extraHtmlFunctions import statusCodeInfo, errorBrokenLink, longName
from Checks.linkCheck import linkCheck
from pprint import pprint

def generateLinksHtml(myCanvas, canvasQa):
    
    linksData = {}
    linksData['Page'] = {}
    linksData['Quiz'] = {}
    
    for pageId, pageData in canvasQa['pages'].items():
        if pageData.get('links') == None:
            continue
        linksData['Page'][pageId] = {}
        linksData['Page'][pageId]['title'] = pageData['title']
        linksData['Page'][pageId]['url'] = pageData['url']
        linksData['Page'][pageId]['links'] = pageData['links']
        
    for assessmentGroupId, assessmentGroupData in canvasQa['assignments'].items():
        for assessmentId, assessmentData in assessmentGroupData['assignments'].items():
            if 'online_quiz' not in assessmentData['submissionTypes']:
                continue
            for questionId, quizData in assessmentData['quiz'].items():
                if quizData['links'] == None:
                    continue
                linksData['Quiz'][assessmentId] = {}
                linksData['Quiz'][assessmentId]['title'] = assessmentData['title']
                linksData['Quiz'][assessmentId]['url'] = assessmentData['url']
                linksData['Quiz'][assessmentId]['links'] = quizData['links']
                
    if linksData.get('Page') is None and linksData.get('Quiz') is None:
        return ''
    htmllinks = htmlLinksGenerate(linksData, canvasQa['issues']['Course Links']['id'], myCanvas) 
    
    return htmllinks

def htmlLinksGenerate(linksData, id, myCanvas):
    html = (
            Article([Class('message')],
                Div([Class('message-header')],
                    P([], Span([], 'Course Links'),
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
                                htmlLinksAccordian(linksData
                            , myCanvas)
                            ), 
                            #about('Course Links', getDescriptions('Course Links'))
                        )
                    )
                )
            ),
        )    
    return html

def htmlLinksAccordian(linksData, myCanvas):
    html = ''
    for key, values in linksData.items():
        if len(values) == 0:
            continue
        html = (html,
                    Table([Class('table')],
                        Thead([],
                            Tr([], 
                                Th([], f'{key} Name'),
                                Th([], '# of Items'),
                                Th([], 'Show/Hide')
                            )
                        ),
                        Tbody([],
                            htmlLinksHeader(values, myCanvas)
                        )
                    )
                )
                
    return html

def htmlLinksHeader(values, myCanvas):
    
    html = ''
    for id, info in sorted(values.items()):
        sumItems = len(info['links']) if info['links'] is not None else 0
        if sumItems == 0:
            continue
        statusCodeErrors = []
        for altTag, source in info['links'].items():
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
                                                Th([], 'Alt Text'),
                                                Th([], 'Source URL'),                                          
                                            )
                                        ),
                                        Tbody([],
                                            htmlLinksItems(info, myCanvas)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
    return html

def htmlLinksItems(info, myCanvas):
    html = ''
    for altTag, source in sorted(info['links'].items(), key=lambda x: x[1]['statusCode']):
        html = (html,
            Tr([],
                Td([], 
                    statusCodeInfo(source['statusCode'])
                ),
                Td([], altTag if altTag is not None else ''),
                Td([Class('is-multiline')], 
                    A([Href(source['source']), Target('_blank'), Rel('noopener noreferrer')], longName(source['source'])))
                ),
            )   
    return html