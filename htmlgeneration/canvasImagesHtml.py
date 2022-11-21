from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions
from htmlgeneration.extraHtmlFunctions import statusCodeInfo
from Checks.linkCheck import linkCheck
from pprint import pprint

def generateImagesHtml(myCanvas, canvasQa):
    canvasQa['issues']['Images'] = { 'id':"collapsible-img-check", 'count' : 0 }
    placeholderIssues = {}
    placeholderIssues['Pages'] = {}
    placeholderIssues['Quizzes'] = {}
    
    for pageId, pageData in canvasQa['pages'].items():
        if pageData.get('placeholders') == None:
            continue
        placeholderIssues['Pages'][pageId] = {}
        placeholderIssues['Pages'][pageId]['title'] = pageData['title']
        placeholderIssues['Pages'][pageId]['url'] = pageData['url']
        placeholderIssues['Pages'][pageId]['images'] = pageData['imgTags']
        #canvasQa['issues']['Placeholders']['count'] += len(pageData['placeholders']) if pageData['placeholders'] is not None else 0
        
    for assessmentGroupId, assessmentGroupData in canvasQa['assignments'].items():
        for assessmentId, assessmentData in assessmentGroupData['assignments'].items():
            if 'online_quiz' not in assessmentData['submissionTypes']:
                continue
            for questionId, quizData in assessmentData['quiz'].items():
                if quizData['placeholders'] == None:
                    continue
                placeholderIssues['Quizzes'][assessmentId] = {}
                placeholderIssues['Quizzes'][assessmentId]['title'] = assessmentData['title']
                placeholderIssues['Quizzes'][assessmentId]['url'] = assessmentData['url']
                placeholderIssues['Quizzes'][assessmentId]['images'] = quizData['imgTags']
                #canvasQa['issues']['Placeholders']['count'] += len(quizData['placeholders']) if quizData['placeholders'] is not None else 0
    htmlPlaceholders = htmlImagesGenerate(placeholderIssues, canvasQa['issues']['Images']['id'], myCanvas)
    
    return htmlPlaceholders

def htmlImagesGenerate(placeholderIssues, id, myCanvas):
    html = (
            Article([Class('message')],
                Div([Class('message-header')],
                    P([], Span([], 'Images'),
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
                        Div([Class('columns is-multiline')],
                            Div([Class('column is-8 is-narrow')],
                                htmlImagesAccordian(placeholderIssues, myCanvas)
                            ), 
                            about('Placeholders Check', getDescriptions('Placeholder'))
                        )
                    )
                )
            ),
        )    
    return html

def htmlImagesAccordian(placeholderIssues, myCanvas):
    html = ''
    for key, values in placeholderIssues.items():
        if len(values) == 0:
            continue
        html = (html,
                    Table([Class('table')],
                        Thead([],
                            #P([], Em([], ['This is a list of any Blackboard Terms used in the course and associated items'])),
                            #P([], Em([], ['These will need to be changed to reflect tools used in Canvas'])),
                            Tr([], 
                                Th([], f'{key} Name'),
                                Th([], '# of Items'),
                                Th([], 'Show/Hide')
                            )
                        ),
                        htmlImagesHeader(values, myCanvas)
                    )
                )
                
    return html

def htmlImagesHeader(values, myCanvas):
    
    html = ''
    for id, info in sorted(values.items()):
        sumIssues = len(info['images']) if info['images'] is not None else 0
        if sumIssues == 0:
            continue
        html = (html,
            Tbody([],
                Tr([],
                    Td([], 
                        A([Href(info['url']), Target('_blank'), Rel('noopener noreferrer')], info['title']),
                    ),
                    Td([], str(sumIssues)),
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
                                        htmlImagesItems(info, myCanvas)
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    return html

def htmlImagesItems(info, myCanvas):
    html = ''
    for altTag, source in info['images'].items():
        html = (html,
        Tbody([],
            Tr([],
                Td([], 
                    statusCodeInfo(source['statusCode'])#linkCheck(source['statusCode'], myCanvas))
                ),
                Td([], altTag if altTag is not None else ''),
                Td([], 
                    A([Href(source['source']), Target('_blank'), Rel('noopener noreferrer')], source['source']))
                ),
            )   
        )
    return html