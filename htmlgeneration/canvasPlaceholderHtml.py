from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from htmlgeneration.extraHtmlFunctions import placeholderSummary
from lib.InfoPacks import getDescriptions
from pprint import pprint

def generatePlaceholderHtml(myCanvas, canvasQa):
    
    placeholderIssues = {}
    placeholderIssues['Pages'] = {}
    placeholderIssues['Quizzes'] = {}
    placeholderIssues['Assignments'] = {}
    
    for pageId, pageData in canvasQa['pages'].items():
        if pageData.get('placeholders') == None:
            continue
        placeholderIssues['Pages'][pageId] = {}
        placeholderIssues['Pages'][pageId]['title'] = pageData['title']
        placeholderIssues['Pages'][pageId]['url'] = pageData['url']
        placeholderIssues['Pages'][pageId]['placeholders'] = pageData['placeholders']
        canvasQa['issues']['Placeholders']['count'] += len(pageData['placeholders']) if pageData['placeholders'] is not None else 0
        
    for assessmentGroupId, assessmentGroupData in canvasQa['assignments'].items():
        for assessmentId, assessmentData in assessmentGroupData['assignments'].items():
            if assessmentData['submissionTypes'] == 'Online Quiz':
                for questionId, quizData in assessmentData['quiz'].items():
                    if quizData['placeholders'] == None:
                        continue
                    placeholderIssues['Quizzes'][assessmentId] = {}
                    placeholderIssues['Quizzes'][assessmentId]['title'] = assessmentData['title']
                    placeholderIssues['Quizzes'][assessmentId]['url'] = assessmentData['url']
                    placeholderIssues['Quizzes'][assessmentId]['placeholders'] = quizData['placeholders']
                    canvasQa['issues']['Placeholders']['count'] += len(quizData['placeholders']) if quizData['placeholders'] is not None else 0
            
            if assessmentData.get('placeholders', None) == None:
                continue
            placeholderIssues['Assignments'][assessmentId] = {}
            placeholderIssues['Assignments'][assessmentId]['title'] = assessmentData['title']
            placeholderIssues['Assignments'][assessmentId]['url'] = assessmentData['url']
            placeholderIssues['Assignments'][assessmentId]['placeholders'] = assessmentData['placeholders']
            canvasQa['issues']['Placeholders']['count'] += len(assessmentData['placeholders']) if assessmentData['placeholders'] is not None else 0
    if canvasQa['issues']['Placeholders']['count'] < 1:
        return ''            
    if placeholderIssues.get('Pages') is None and placeholderIssues.get('Quizzes') is None and placeholderIssues.get('Assignments') is None:
        return ''
    htmlPlaceholders = htmlPlaceholdersGenerate(placeholderIssues, canvasQa['issues']['Placeholders']['id'], canvasQa)
    
    return htmlPlaceholders

def htmlPlaceholdersGenerate(placeholderIssues, id, canvasQa):
    html = (
            Article([Class('message')],
                Div([Class('message-header')],
                    P([], Span([], 'Placeholders'), placeholderSummary(canvasQa['issues']['Placeholders']['count']),
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
                                htmlPlaceholdersAccordian(placeholderIssues)
                            ), 
                        )
                    )
                )
            ),
        )    
    return html

def htmlPlaceholdersAccordian(placeholderIssues):
    html = ''
    for key, values in placeholderIssues.items():
        if len(values) == 0:
            continue
        html = (html,
                    Table([Class('table')],
                        Thead([],
                            P([], Em([], ['A placeholder is a term/phrase used inside of a Canvas Course site to indicate work still to be done.<br>'\
                                        "The table shows indicates a distinction between placeholders created by Word 2 Canvas and those created by someone manually within the course."])),
                            
                            Tr([], 
                                Th([], f'{key} Name'),
                                Th([], '# of Items'),
                                Th([], 'Show/Hide')
                            )
                        ),
                        Tbody([],
                            htmlPlaceholdersHeader(values)
                        )
                    )
                )
                
    return html

def htmlPlaceholdersHeader(values):
    
    html = ''
    for id, info in sorted(values.items()):
        sumIssues = len(info['placeholders']) if info['placeholders'] is not None else 0
        if sumIssues == 0:
            continue
        html = (html,
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
                                                Th([], 'Issue Type'),
                                                Th([], 'Information Text'),                                          
                                            )
                                        ),
                                        Tbody([],
                                            htmlPlaceholdersItems(info)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
    return html

def htmlPlaceholdersItems(info):
    html = ''
    for issueType, infoText in info['placeholders'].items():
        html = (html,
            Tr([],
                Td([], issueType if issueType is not None else ''),
                Td([], infoText if infoText is not None else ''),
                ),
            )   
    return html