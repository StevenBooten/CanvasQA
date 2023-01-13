from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style


def generateContentsTable(canvasQa):

    html = (
            Table([ Class('table')],
                Thead([Class('table-header has-text-is-medium')],
                    Tr([],
                        Th([], 'Catagory Name'),
                        Th([Class('has-text-centered')], 'Flagged Issue Count'),
                        )
                    ),
                    Tbody([],
                        contentsTableBody(canvasQa['issues']),
                    )
                )
            )
            
    return html

def contentsTableBody(issueList):
    html = ''
    
    for title, value in sorted(issueList.items(), key=lambda x: x[1]['count'], reverse=True):
        
        if value['count'] > 0 or title not in ['Unattached Pages', 'Blackboard Residuals', 'Placeholders']:
            html = (html,
                    Tr([],
                        Td([Class('is-size-7')],
                            A([Onclick(f'sectionExpand("{value["id"]}");')], title)
                        ),
                        Td([Class('is-size-7 has-text-centered')], str(value['count'])) if value['count'] > 0 else Td([Class('is-size-7 has-text-centered')], 'None')
                        )
                    )
    return html