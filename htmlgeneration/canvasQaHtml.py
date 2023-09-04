from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from datetime import datetime, timedelta
from htmlgeneration.canvasModulesHtml import generateModulesHtml
from htmlgeneration.canvasFilesHtml import generateFileStructureHtml
from htmlgeneration.canvasPlaceholderHtml import generatePlaceholderHtml
#from htmlgeneration.deprecated.CanvasBBIssuesHtml import generateBBIssuesHtml
from htmlgeneration.canvasImagesHtml import generateImagesHtml
from htmlgeneration.canvasUnattachedPageshtml import generateUnattachedPagesHtml
from htmlgeneration.canvasAssignmentsHtml import generateAssignmentHtml
from htmlgeneration.canvasLinksHtml import generateLinksHtml
from htmlgeneration.canvasEmbeddedContentHtml import generateEmbeddedContentHtml
from htmlgeneration.canvasSummaryHtml import generateContentsTable
import sys
import io
from pprint import pprint

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def generateQaHtml(myCanvas, canvasQa):
    dateNow = datetime.now()
    runDate = dateNow.strftime("%d %B")
    runTime = dateNow.strftime("%I:%M %p")
    dateUpdate = dateNow + timedelta(days=1)
    updateDate = dateUpdate.strftime("%d-%B")
    updateTime = dateUpdate.strftime("%I:%M %p")
    
    generatedHtml = {}
    generatedHtml['Modules'] = generateModulesHtml(myCanvas, canvasQa)
    generatedHtml['File Structure'] = generateFileStructureHtml(myCanvas, canvasQa)
    #generatedHtml['Blackboard Residuals'] = generateBBIssuesHtml(myCanvas, canvasQa)
    generatedHtml['Placeholders'] = generatePlaceholderHtml(myCanvas, canvasQa)
    generatedHtml['Images'] = generateImagesHtml(myCanvas, canvasQa)
    generatedHtml['Unattached Pages'] = generateUnattachedPagesHtml(myCanvas, canvasQa)
    generatedHtml['Assignments'] = generateAssignmentHtml(myCanvas, canvasQa)
    generatedHtml['Course Links'] = generateLinksHtml(myCanvas, canvasQa)
    generatedHtml['Embedded Content'] = generateEmbeddedContentHtml(myCanvas, canvasQa)
    htmlContentsTable = generateContentsTable(canvasQa)
    
    #create the string of ID's for the JS to use
    accordianIds = ''
    for key, value in canvasQa['issues'].items():
        accordianIds += f'"{value["id"]}",'
    
    
    jsScript = "function sectionExpand(id) {\n" + \
        "const collapsible = document.getElementById(id);\n" + \
        f'const linkList = [{accordianIds}];\n' + \
        'if (collapsible.getAttribute("aria-expanded") === "false") {\n' + \
        "    console.log('found it');\n" + \
        "    //scroll to collapsible\n" + \
        "    //collapsible.scrollIntoView(true);\n" + \
        "    let url = location.toString();\n" + \
        "    url = url.split('#')[0];\n" + \
        "    //remove the X and everything after it\n" + \
        "    console.log(location);\n" + \
        "    location = url + '#' + id;\n" + \
        "    for (let i = 0; i < linkList.length; i++) {\n" + \
        "        let link = document.getElementById(linkList[i]);\n" + \
        "        if (link) {\n" + \
        "            link.bulmaCollapsible('close');\n" + \
        "            }\n" + \
        "        }\n" + \
        "    collapsible.bulmaCollapsible('open');\n" + \
        "    setTimeout(() => {  console.log('Opened'); }, 5000);\n" + \
        "    collapsible.scrollIntoView(true);\n" + \
        "} else {\n" + \
        "    collapsible.bulmaCollapsible('close');\n" + \
        "}" + \
    "}"
    
    html = Html([Lang("en")],
        Head([],
            Link([Rel("stylesheet"), Href("https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css")]),
            Link([Rel("stylesheet"), Href("https://cdn.jsdelivr.net/npm/@creativebulma/bulma-collapsible@1.0.4/dist/css/bulma-collapsible.min.css")]),
            Link([Rel("stylesheet"), Href("https://cdn.jsdelivr.net/npm/@creativebulma/bulma-tooltip@1.2.0/dist/bulma-tooltip.min.css")]),
            Meta([Name("viewport"), Content("width=device-width, initial-scale=1")]),
            Script([Src("https://cdn.jsdelivr.net/npm/@creativebulma/bulma-collapsible@1.0.4/dist/js/bulma-collapsible.min.js")]),
            Link([Rel("stylesheet"), Href("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css")]),
            Link([Rel("stylesheet"), Type('text/css'), Href("https://cdn.datatables.net/v/dt/dt-1.13.1/datatables.min.css")]),
            Script([Type('text/javascript'), Src("https://cdn.datatables.net/v/dt/dt-1.13.1/datatables.min.js")]),
            ),
            
            Body([],
            Section([Class('section')],
                    P([Class('header'), Style('font-size:10px')],  [f'This report was automatically generated {runDate} at {runTime}<br>Canvas QA designed and built by'],
                        A([Href('mailto:s.booten@griffith.edu.au'), Target('_blank'), Rel('noopener noreferrer')], 'Steven Booten'),
                Script([], f'{jsScript}'), '<br><br>',
                
                
                H1([Id('top'), Class('title')], [f'Quality Assurance report for Canvas Course Site: {myCanvas.courseCode.replace("_"," ")}']),
                
                Div([Class('content')],
                    Div([Class('columns is-multiline')],
                        Div([Class('column is-2')],
                            htmlContentsTable,
                        )
                    )
                    #    ),
                    #    Div([Class('column is-1')]),
                    #    Div([Class('column')],
                    #        '<br>',
                    #        Head([Class('message-header is-size-5 has-text-weight-bold')], 'Heuristics'),
                    #            Ul([],
                    #                Li([Class('is-size-7')], ['The side navigation is refined to necessary course links and are organised so mutual content is next to each other (ie. content and assessment).']),
                    #                Li([Class('is-size-7')], ['The modules are easy to follow and not overwhelming to scroll through.']),
                    #                Li([Class('is-size-7')], ['The page accurately presents content that is clear and easy to follow.']),
                    #                Li([Class('is-size-7')], ['The discussions has been set up correctly.']),
                    #                Li([Class('is-size-7')], ['The content is accessible to those using screen-readers.']),
                    #                Li([Class('is-size-7')], ['The library areas (Files, Pages, Studio) of the course site are organised and articulate of the content they hold ']),
                    #                Li([Class('is-size-7')], ['When viewed as a student, the student experience is as expected with clear wayfinding and links/LTIs working as intended.'])
                    #            )  
                    #        )  
                    #    ),
                    ),
                    [generatedHtml[key] for key, value in sorted(canvasQa['issues'].items(), key=lambda x: x[1]['count'], reverse=True)],
                ), 
            )
        ),
        Script([], 'bulmaCollapsible.attach()'),
        
    )
    """Div([Class('modal)')],
            Div([Class('modal-background')]),
            Div([Class('modal-card')],
                Header([Class('modal-card-head')],
                        P([Class('modal-card-title')], 'Modal title'),
                        Button([Class('delete'), Aria_('lable', 'close')]),                       
                    ),
                Section([Class('modal-card-body')],
                        'Stuff and things'
                    ),
                Footer([Class('modal-card-foot')],
                    Button([Class('button is-success')], 'Save changes'),
                    Button([Class('button')], 'Cancel')
                    )
                )
            )"""
    
    return html





