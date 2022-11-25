from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions
from htmlgeneration.extraHtmlFunctions import statusCodeInfo, errorBrokenLink
from Checks.linkCheck import linkCheck
from pprint import pprint

def generateImagesHtml(myCanvas, canvasQa):
    
    imagesData = {}
    imagesData['Page'] = {}
    imagesData['Quiz'] = {}
    
    for pageId, pageData in canvasQa['pages'].items():
        if pageData.get('imgTags') == None:
            continue
        imagesData['Page'][pageId] = {}
        imagesData['Page'][pageId]['title'] = pageData['title']
        imagesData['Page'][pageId]['url'] = pageData['url']
        imagesData['Page'][pageId]['images'] = pageData['imgTags']
        
    for assessmentGroupId, assessmentGroupData in canvasQa['assignments'].items():
        for assessmentId, assessmentData in assessmentGroupData['assignments'].items():
            if 'online_quiz' not in assessmentData['submissionTypes']:
                continue
            for questionId, quizData in assessmentData['quiz'].items():
                if quizData['imgTags'] == None:
                    continue
                imagesData['Quiz'][assessmentId] = {}
                imagesData['Quiz'][assessmentId]['title'] = assessmentData['title']
                imagesData['Quiz'][assessmentId]['url'] = assessmentData['url']
                imagesData['Quiz'][assessmentId]['images'] = quizData['imgTags']
                
    if imagesData.get('Page') is None and imagesData.get('Quiz') is None:
        return ''
    htmlImages = htmlImagesGenerate(imagesData, canvasQa['issues']['Images']['id'], myCanvas) 
    
    return htmlImages

def htmlImagesGenerate(imagesData, id, myCanvas):
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
                        Div([Class('columns')],
                            Div([Class('column')],
                                htmlImagesAccordian(imagesData
                            , myCanvas)
                            ), 
                            #about('Placeholders Check', getDescriptions('Placeholder'))
                        )
                    )
                )
            ),
        )    
    return html

def htmlImagesAccordian(imagesData, myCanvas):
    html = ''
    for key, values in imagesData.items():
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
                        Tbody([],
                            htmlImagesHeader(values, myCanvas)
                        )
                    )
                )
                
    return html

def htmlImagesHeader(values, myCanvas):
    
    html = ''
    for id, info in sorted(values.items()):
        sumItems = len(info['images']) if info['images'] is not None else 0
        if sumItems == 0:
            continue
        statusCodeErrors = []
        for altTag, source in info['images'].items():
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
    for altTag, source in sorted(info['images'].items(), key=lambda x: x[1]['statusCode']):
        html = (html,
            Tr([],
                Td([], 
                    statusCodeInfo(source['statusCode'])
                ),
                Td([], altTag if altTag is not None else ''),
                Td([], 
                    A([Href(source['source']), Target('_blank'), Rel('noopener noreferrer')], source['source']))
                ),
            )
    return html