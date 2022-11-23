from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions
from pprint import pprint


def generateBBIssuesHtml(myCanvas, canvasQa):
    canvasQa['issues']['Blackboard Residuals'] = { 'id':"collapsible-bb-check", 'count' : 0 }
    bbIssues = {}
    bbIssues['Pages'] = {}
    bbIssues['Quizzes'] = {}
    
    for pageId, pageData in canvasQa['pages'].items():
        if pageData.get('bbTerms') == None and pageData.get('bbEcho') == None and pageData.get('bbHtml') == None:
            continue
        bbIssues['Pages'][pageId] = {}
        bbIssues['Pages'][pageId]['title'] = pageData['title']
        bbIssues['Pages'][pageId]['url'] = pageData['url']
        bbIssues['Pages'][pageId]['bbTerms'] = pageData['bbTerms']
        bbIssues['Pages'][pageId]['bbEcho'] = pageData['bbEcho']
        bbIssues['Pages'][pageId]['bbHtml'] = pageData['bbHtml']
        canvasQa['issues']['Blackboard Residuals']['count'] += len(pageData['bbTerms']) if pageData['bbTerms'] is not None else 0
        canvasQa['issues']['Blackboard Residuals']['count'] += len(pageData['bbEcho']) if pageData['bbEcho'] is not None else 0
        canvasQa['issues']['Blackboard Residuals']['count'] += len(pageData['bbHtml']) if pageData['bbHtml'] is not None else 0
        
    for assessmentGroupId, assessmentGroupData in canvasQa['assignments'].items():
        for assessmentId, assessmentData in assessmentGroupData['assignments'].items():
            if 'online_quiz' not in assessmentData['submissionTypes']:
                continue
            for questionId, quizData in assessmentData['quiz'].items():
                if quizData['bbTerms'] == None and quizData['bbEcho'] == None and quizData['bbHtml'] == None:
                    continue
                bbIssues['Quizzes'][assessmentId] = {}
                bbIssues['Quizzes'][assessmentId]['title'] = assessmentData['title']
                bbIssues['Quizzes'][assessmentId]['url'] = assessmentData['url']
                bbIssues['Quizzes'][assessmentId]['bbTerms'] = quizData['bbTerms']
                bbIssues['Quizzes'][assessmentId]['bbEcho'] = quizData['bbEcho']
                bbIssues['Quizzes'][assessmentId]['bbHtml'] = quizData['bbHtml']
                canvasQa['issues']['Blackboard Residuals']['count'] += len(quizData['bbTerms']) if quizData['bbTerms'] is not None else 0
                canvasQa['issues']['Blackboard Residuals']['count'] += len(quizData['bbEcho']) if quizData['bbEcho'] is not None else 0
                canvasQa['issues']['Blackboard Residuals']['count'] += len(quizData['bbHtml']) if quizData['bbHtml'] is not None else 0
                
    if bbIssues.get('Pages') is None and bbIssues.get('Quizzes') is None:
        return ''
    htmlBBIssues = htmlBBIssuesGenerate(bbIssues, canvasQa['issues']['Blackboard Residuals']['id'])
    
    return htmlBBIssues


def htmlBBIssuesGenerate(bbIssues, id):
    
    html = ''
    html = (html, 
                Article([Class('message')],
                    Div([Class('message-header')],
                        P([], Span([], 'Blackboard Residuals'), #accordionError(len(qaInfo.bbTermsInPages.values())),
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
                            Div([Class('columns is-multiline')],
                                Div([Class('column is-8 is-narrow')],
                                    htmlBBIssuesAccordian(bbIssues)
                                ), 
                                about('Blackboard Issues Check', getDescriptions('Blackboard Terms'))
                            )
                        )
                    )
                ),
            )    
    return html

def htmlBBIssuesAccordian(bbIssues):
    html = ''
    for key, values in bbIssues.items():
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
                        bbIssuesHtml(values)
                    )
                )
                
    return html

def bbIssuesHtml(values):
    
    keys = ['bbTerms', 'bbEcho', 'bbHtml']
    html = ''
    for id, info in sorted(values.items()):
        sumIssues = 0
        for key in keys:
            sumIssues += len(info[key]) if info[key] is not None else 0
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
                                    A([Href(f'#collapsible-items-bb-{id}'), Data_('action','collapse')], 'Show Items')
                                )
                            ),
                            Tr([Id(f'collapsible-items-bb-{id}'), Class('is-collapsible')],
                                Td([Colspan('6')],
                                    Div([],
                                        Div([Id(f'collapsible-items-bb-{id}'), Class('is-collapsible')],
                                            Table([Class('table is-fullwidth is-bordered is-striped is-size-7')],
                                                Thead([],
                                                    Tr([], 
                                                        Th([], 'Issue Type'),
                                                        Th([], 'Issue Term'),
                                                        Th([], 'Associated Text')                                           
                                                    )
                                                ),
                                                bbIssuesItems(info, keys)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
    return html

def bbIssuesItems(info, keys):
    html = ''
    issueType = {'bbTerms': 'Blackboard Term Found', 'bbEcho': 'Blackboard Echo Found', 'bbHtml': 'Blackboard Html Artifact'}
    for key in keys:
        if info[key] is None:
            continue
        for text, source in info[key].items():
            html = (html,
                        Tbody([],
                            Tr([],
                                Td([], issueType[key]),
                                Td([], text if text is not None else ''),
                                Td([], source if source is not None else ''),
                                ),
                            )   
                        )
    return html
