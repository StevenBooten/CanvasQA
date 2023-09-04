from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style as InlineStyle
from Checks.linkCheck import linkCheck
from htmlgeneration.extraHtmlFunctions import about
from lib.InfoPacks import getDescriptions
#from htmlgeneration.extraHtmlFunctions import AssignmentFolderError


def generateAssignmentHtml(myCanvas, canvasQa):
    
    if canvasQa.get('assignments') is None:
        return ''
    htmlAssignment = AssignmentAccordian(canvasQa, canvasQa['issues']['Assignments']['id']) if len(canvasQa['assignments']) > 0 else ''
    
    return htmlAssignment
    
def AssignmentAccordian(canvasQa, id):
    
    html = ''
    html = (   
        Article([Class('message')],
            Div([Class('message-header')],
                P([], Span([], 'Assignments'), #accordionError(qaInfo.errorFiles['total']),
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
                    Div([Class('columns is-multiline is-variable is-8')],
                        Div([Class('column')],
                            Div([Class('table-container')],
                                Table([Class('table')],
                                    Thead([],
                                            P([], Em([], ['This is a complete breakdown of the Courses Assignment Structure by Assignment Group<br>' \
                                                            'Under each assignment group will be a breakdown of each assignment in that group and relavent information from Canvas.<br>' \
                                                            'If an assignment is a quiz there will be a third level showing the questions in that quiz,<br>' \
                                                            'with a breakdown of relevant data points from Canvas and any errors found in each question.'])), 
                                        Tr([], 
                                            Th([], 'Assignment Group'),
                                            Th([], '# of Assessment Items'),
                                            Th([], 'Weighting'),
                                            Th([], 'Show/Hide')
                                        )
                                    ),
                                    Tbody([],
                                        AssignmentHtml(canvasQa['assignments'])
                                    )
                                )
                            )
                        ),
                    )
                )
            )  
        )    
    )                     
    
    return html

def AssignmentHtml(assignments):
    
    html = ''
    for key, values in assignments.items():
        html = (html,
                Tr([],
                    Td([],
                        A([Href(values['url']), Target('_blank'), Rel('noopener noreferrer')], values['title']), #AssignmentFolderError(items['files']), 
                    ),
                    Td([], str(len(values['assignments']))),
                    Td([], str(values['weight'])+"%"),
                    Td([],
                        Span([Class('tag is-info is-size-7')],
                            A([Href(f'#collapsible-items-{key}-assignments'), Data_('action','collapse')], 'Show Assignments') 
                            if len(values['assignments']) > 0 else 'No Assignments'
                            
                        )
                    ),
                    Tr([Id(f'collapsible-items-{key}-assignments'), Class('is-collapsible')],
                        Td([Colspan('6')],
                            Div([],
                                Div([Id(f'collapsible-items-{key}-assignments'), Class('is-collapsible')],
                                    Table([Class('table is-fullwidth is-bordered is-striped is-size-7')],
                                        Thead([],
                                            Tr([], 
                                                Th([], 'Assessment Title'),
                                                Th([], 'Submission Type'),
                                                Th([], 'Max Score'),
                                                Th([], 'Published'), 
                                                Th([], 'Rubric'),
                                                Th([], 'Quiz Questions'),               
                                            )
                                        ),
                                        Tbody([],
                                            AssignmentItems(values['assignments']) 
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        
    return html

def AssignmentItems(items):
    html = ''
    for key, item in items.items():
        
        html = (html,
                Tr([],
                    Td([],
                    A([Href(item['url']), Target('_blank'), Rel('noopener noreferrer')], item['title']),
                    ),
                    Td([], item['submissionTypes']),
                    Td([], str(item['points'])),
                    Td([], 'Yes' if item['published'] is True else 'No'),
                    Td([], 'Yes' if item['rubric'] is not None else 'No'),
                    Td([],  
                        Span([Class('tag is-info is-size-7')],
                            A([Href(f'#collapsible-items-{key}-quizzes'), Data_('action','collapse')], f'{item.get("questionCount", 0)} Questions')
                        ) if item.get("questionCount", 0) > 0 else 'Quiz has 0 Questions' if item.get('quiz', None) is not None else '-'
                    ), quizQuestionHtml(item['quiz'], key, item.get("questionCount", 0)) if item.get('quiz', None) is not None else '' 
                ),  
            )
            
    return html

def quizQuestionHtml(questions, key, questionCount):
    
    html = (
            Tr([Id(f'collapsible-items-{key}-quizzes'), Class('is-collapsible')],
                Td([Colspan('6')],
                    Div([],
                        Div([Id(f'collapsible-items-{key}-quizzes'), Class('is-collapsible')],
                            Table([Class('table is-fullwidth is-bordered is-striped is-size-7')],
                                Thead([],
                                    Tr([], 
                                        Th([], 'Question Title'),
                                        Th([], 'Question Type'),
                                        Th([], 'Points'),
                                        Th([], 'Has Correct Answer'),            
                                    )
                                ),
                                Tbody([],
                                    questionItems(questions, questionCount) 
                                )
                            )
                        )
                    )
                )
            )
        )

    return html

def questionItems(items, questionCount):
    html = ''
    if len(items) < 1:
        html = (
                Tr([],
                    Td([Colspan('6')], 'Questions pulled from Question Bank. Unable to list details.'),
                )
            )
        
    for key, item in items.items():
        
        html = (
                Tr([],
                    Td([], item['title'] if item['title'] is not None else 'No Title'),
                    Td([], item['questionType'].replace('_', ' ').capitalize()),
                    Td([], str(item['points'])),
                    Td([], 'Yes' if item['hasCorrectAnswer'] is True else 'No'),
                ),    
            )
    return html