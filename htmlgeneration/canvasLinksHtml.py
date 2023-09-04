from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions
from htmlgeneration.extraHtmlFunctions import statusCodeInfo, errorBrokenLink, longName, statusErrorSummary
from Checks.linkCheck import linkCheck
from pprint import pprint

def generateLinksHtml(myCanvas, canvasQa):
    
    linksData = {}
    linksData['Page'] = {}
    linksData['Quiz'] = {}
    linksData['Assignment'] = {}
    
    canvasQa['issues']['Course Links']['Summary'] = {}
    
    for pageId, pageData in canvasQa['pages'].items():
        if pageData.get('links') == None:
            continue
        linksData['Page'][pageId] = {}
        linksData['Page'][pageId]['title'] = pageData['title']
        linksData['Page'][pageId]['url'] = pageData['url']
        linksData['Page'][pageId]['links'] = pageData['links']
        
        for altTag, data in pageData['links'].items():
            canvasQa['issues']['Course Links']['Summary']['total'] = canvasQa['issues']['Course Links']['Summary'].get('total', 0) + 1
            if data['statusCode'] == 0:
                canvasQa['issues']['Course Links']['Summary']['errors'] = canvasQa['issues']['Course Links']['Summary'].get('errors', 0) + 1
            elif data['statusCode'] < 200:
                canvasQa['issues']['Course Links']['Summary']['warning'] = canvasQa['issues']['Course Links']['Summary'].get('warning', 0) + 1
            elif data['statusCode'] < 300:
                canvasQa['issues']['Course Links']['Summary']['good'] = canvasQa['issues']['Course Links']['Summary'].get('good', 0) + 1
            elif data['statusCode'] < 400:
                canvasQa['issues']['Course Links']['Summary']['warning'] = canvasQa['issues']['Course Links']['Summary'].get('warning', 0) + 1
            else:
                canvasQa['issues']['Course Links']['Summary']['errors'] = canvasQa['issues']['Course Links']['Summary'].get('errors', 0) + 1
            
            
        
    for assessmentGroupId, assessmentGroupData in canvasQa['assignments'].items():
        for assessmentId, assessmentData in assessmentGroupData['assignments'].items():
            if 'online_quiz' in assessmentData['submissionTypes']:
                for questionId, quizData in assessmentData['quiz'].items():
                    if quizData['links'] == None:
                        continue
                    linksData['Quiz'][assessmentId] = {}
                    linksData['Quiz'][assessmentId]['title'] = assessmentData['title']
                    linksData['Quiz'][assessmentId]['url'] = assessmentData['url']
                    linksData['Quiz'][assessmentId]['links'] = quizData['links']
                    
                    for altTag, data in quizData['links'].items():
                        canvasQa['issues']['Course Links']['Summary']['total'] = canvasQa['issues']['Course Links']['Summary'].get('total', 0) + 1
                        if data['statusCode'] == 0:
                            canvasQa['issues']['Course Links']['Summary']['errors'] = canvasQa['issues']['Course Links']['Summary'].get('errors', 0) + 1
                        elif data['statusCode'] < 200:
                            canvasQa['issues']['Course Links']['Summary']['warning'] = canvasQa['issues']['Course Links']['Summary'].get('warning', 0) + 1
                        elif data['statusCode'] < 300:
                            canvasQa['issues']['Course Links']['Summary']['good'] = canvasQa['issues']['Course Links']['Summary'].get('good', 0) + 1
                        elif data['statusCode'] < 400:
                            canvasQa['issues']['Course Links']['Summary']['warning'] = canvasQa['issues']['Course Links']['Summary'].get('warning', 0) + 1
                        else:
                            canvasQa['issues']['Course Links']['Summary']['errors'] = canvasQa['issues']['Course Links']['Summary'].get('errors', 0) + 1
            else:
                if assessmentData['links'] == None:
                        continue
                linksData['Assignment'][assessmentId] = {}
                linksData['Assignment'][assessmentId]['title'] = assessmentData['title']
                linksData['Assignment'][assessmentId]['url'] = assessmentData['url']
                linksData['Assignment'][assessmentId]['links'] = assessmentData['links']
                
                for altTag, data in assessmentData['links'].items():
                    canvasQa['issues']['Course Links']['Summary']['total'] = canvasQa['issues']['Course Links']['Summary'].get('total', 0) + 1
                    if data['statusCode'] == 0:
                        canvasQa['issues']['Course Links']['Summary']['errors'] = canvasQa['issues']['Course Links']['Summary'].get('errors', 0) + 1
                    elif data['statusCode'] < 200:
                        canvasQa['issues']['Course Links']['Summary']['warning'] = canvasQa['issues']['Course Links']['Summary'].get('warning', 0) + 1
                    elif data['statusCode'] < 300:
                        canvasQa['issues']['Course Links']['Summary']['good'] = canvasQa['issues']['Course Links']['Summary'].get('good', 0) + 1
                    elif data['statusCode'] < 400:
                        canvasQa['issues']['Course Links']['Summary']['warning'] = canvasQa['issues']['Course Links']['Summary'].get('warning', 0) + 1
                    else:
                        canvasQa['issues']['Course Links']['Summary']['errors'] = canvasQa['issues']['Course Links']['Summary'].get('errors', 0) + 1
                
    if linksData.get('Page') is None and linksData.get('Quiz') is None and linksData.get('Assignment') is None:
        return ''
    htmllinks = htmlLinksGenerate(linksData, canvasQa['issues']['Course Links']['id'], myCanvas, canvasQa) 
    
    return htmllinks

def htmlLinksGenerate(linksData, id, myCanvas, canvasQa):
    html = (
            Article([Class('message')],
                Div([Class('message-header')],
                    P([], Span([], 'Course Links'), statusErrorSummary(canvasQa['issues']['Course Links']['Summary']),
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
                            P([], Em([], ['This is a collection of the all links found in the course broken down by course page.<br> '\
                                    'Shows you the status and relevant information for each link.'])),
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