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
    imagesData = {}
    imagesData['Pages'] = {}
    imagesData['Quizzes'] = {}
    
    for pageId, pageData in canvasQa['pages'].items():
        if pageData.get('imgTags') == None:
            continue
        imagesData['Pages'][pageId] = {}
        imagesData['Pages'][pageId]['title'] = pageData['title']
        imagesData['Pages'][pageId]['url'] = pageData['url']
        imagesData['Pages'][pageId]['images'] = pageData['imgTags']
        
    for assessmentGroupId, assessmentGroupData in canvasQa['assignments'].items():
        for assessmentId, assessmentData in assessmentGroupData['assignments'].items():
            if 'online_quiz' not in assessmentData['submissionTypes']:
                continue
            for questionId, quizData in assessmentData['quiz'].items():
                if quizData['imgTags'] == None:
                    continue
                imagesData['Quizzes'][assessmentId] = {}
                imagesData['Quizzes'][assessmentId]['title'] = assessmentData['title']
                imagesData['Quizzes'][assessmentId]['url'] = assessmentData['url']
                imagesData['Quizzes'][assessmentId]['images'] = quizData['imgTags']
    if imagesData.get('Pages') is None and imagesData.get('Quizzes') is None:
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
                        Div([Class('columns is-multiline')],
                            Div([Class('column is-8 is-narrow')],
                                htmlImagesAccordian(imagesData
                            , myCanvas)
                            ), 
                            about('Placeholders Check', getDescriptions('Placeholder'))
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