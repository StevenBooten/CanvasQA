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
    htmlAssignment = AssignmentAccordian(canvasQa, canvasQa['issues']['Assignments']['id'])
    
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
                    Div([Class('columns is-multiline')],
                        Div([Class('column is-8 is-narrow toggle')],
                            Div([Class('table-container')],
                                Table([Class('table')],
                                    Thead([],
                                            P([], Em([], ['This is a complete breakdown of the file structure in the course.'])), 
                                            P([], Em([], ['Please ensure the structure is logical consistent within the course.'])),
                                        Tr([], 
                                            Th([], 'Assignment Group'),
                                            Th([], '# of Assessment Items'),
                                            Th([], 'Weighting'),
                                            Th([], 'Show/Hide')
                                        )
                                    ),
                                    AssignmentHtml(canvasQa['assignments'])
                                )
                            )
                        ),about('Assignments', getDescriptions('Assignments'))
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
            Tbody([],
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
                                                Th([], 'Quiz Questions'),               
                                            )
                                        ),
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
        
        html = (html, #Html([], html,
                Tbody([],
                    Tr([],
                        Td([],
                        A([Href(item['url']), Target('_blank'), Rel('noopener noreferrer')], item['title']), #errorUnusedFiles(item[6]), errorDuplicateFiles(item[5])
                        ),
                        Td([], ', '.join(item['submissionTypes']).replace('_', ' ').capitalize()),
                        Td([], str(item['points'])),
                        Td([], 'Yes' if item['published'] is True else 'No'),
                        Td([],  
                            Span([Class('tag is-info is-size-7')],
                                A([Href(f'#collapsible-items-{key}-quizzes'), Data_('action','collapse')], f'{item.get("questionCount", 0)} Questions')
                            ) if item.get("questionCount", 0) > 0 else 'Quiz has 0 Questions' if item.get('quiz', None) is not None else 'Not a Quiz'
                        ), quizQuestionHtml(item['quiz'], key, item.get("questionCount", 0)) if item.get('quiz', None) is not None else '' 
                    ),  
                )
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
                                        Th([], 'Migration Issues'), 
                                        Th([], 'BB Residual Issues'),              
                                    )
                                ),
                                questionItems(questions, questionCount) 
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
        html = (html,
                Tbody([],
                    Tr([],
                        Td([Colspan('6')], 'Questions pulled from Question Bank. Unable to list details.'),
                    )
                )
            )
        
    for key, item in items.items():
        
        html = (html,
                Tbody([],
                    Tr([],
                        Td([], item['title'] if item['title'] is not None else 'No Title'), #errorUnusedFiles(item[6]), errorDuplicateFiles(item[5])
                        Td([], item['questionType'].replace('_', ' ').capitalize()),
                        Td([], str(item['points'])),
                        Td([], 'Yes' if item['hasCorrectAnswer'] is True else 'No'),
                        Td([], ', '.join(item['quizIssues'].values()) if len(item['quizIssues'].values()) > 1 else item['quizIssues'].values() if len(item['quizIssues'].values()) == 1 else 'No Migration Issues'),
                        Td([], ', '.join(item['bbBrokenLinks'].values()) if len(item['bbBrokenLinks'].values()) > 1 else item['bbBrokenLinks'].values() if len(item['bbBrokenLinks'].values()) == 1 else 'No BB Residual Issues'),
                    ),    
                )
            )
    return html