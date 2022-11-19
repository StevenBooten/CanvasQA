from htmlBuilder.attributes import *
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, Style
from datetime import datetime, timedelta
from htmlgeneration.canvasModulesHtml import moduleAccordian
from htmlgeneration.canvasFilesHtml import fileStructureAccordian
from htmlgeneration.canvasPlaceholderHtml import generatePlaceholderHtml
from htmlgeneration.CanvasBBIssuesHtml import generateBBIssuesHtml
import sys
import io
from pprint import pprint

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def generateQaHtml(myCanvas, canvasQa):
    dateNow = datetime.now()
    runDate = dateNow.strftime("%d-%B")
    runTime = dateNow.strftime("%I:%M %p")
    dateUpdate = dateNow + timedelta(days=1)
    updateDate = dateUpdate.strftime("%d-%B")
    updateTime = dateUpdate.strftime("%I:%M %p")
           
    
    jsScript = """
    function sectionExpand(id) {
        const collapsible = document.getElementById(id);
        const linkList = ["collapsible-img-check","collapsible-videoembed-check", "collapsible-modules-check", "collapsible-assessments-check", "collapsible-filestructure-check", "collapsible-link-check", "collapsible-placeholder-check", "collapsible-bb-check", "collapsible-span-check", "collapsible-unattachedpages-check", "collapsible-bbecho-check", "collapsible-quizzes-check"];
        if (collapsible.ariaExpanded == "false") {
            console.log('found it');
            //scroll to collapsible
            //collapsible.scrollIntoView(true);
            let url = location.toString();
            url = url.split('#')[0];
            //remove the X and everything after it
            console.log(location);
            location = url + '#' + id;
            for (let i = 0; i < linkList.length; i++) {
                let link = document.getElementById(linkList[i]);
                if (link) {
                    link.bulmaCollapsible('close');
                    }
                }
            collapsible.bulmaCollapsible('open');
            setTimeout(() => {  console.log("Opened"); }, 5000);
            collapsible.scrollIntoView(true);
        } else {
            collapsible.bulmaCollapsible('close');
        }
    }"""
    
    htmlModule = moduleAccordian(myCanvas, canvasQa)
    htmlFileStructure = fileStructureAccordian(myCanvas, canvasQa)
    htmlBBIssues, canvasQa = generateBBIssuesHtml(myCanvas, canvasQa)
    htmlPlaceholders, canvasQa = generatePlaceholderHtml(myCanvas, canvasQa)
    
    html = Html([Lang("en")],
        Head([],
            Link([Rel("stylesheet"), Href("https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css")]),
            Link([Rel("stylesheet"), Href("https://cdn.jsdelivr.net/npm/@creativebulma/bulma-collapsible@1.0.4/dist/css/bulma-collapsible.min.css")]),
            Link([Rel("stylesheet"), Href("https://cdn.jsdelivr.net/npm/@creativebulma/bulma-tooltip@1.2.0/dist/bulma-tooltip.min.css")]),
            Meta([Name("viewport"), Content("width=device-width, initial-scale=1")]),
            Script([Src("https://cdn.jsdelivr.net/npm/@creativebulma/bulma-collapsible@1.0.4/dist/js/bulma-collapsible.min.js")]),
            Link([Rel("stylesheet"), Href("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css")]),
            ),
            
            Body([],
            Section([Class('section')],
                    P([Class('header'), Style('font-size:10px')],  [f'This report was automatically generated {runDate} at {runTime}'],# and will be updated {updateDate} by {updateTime}<br>Canvas QA designed and built by'],
                        A([Href('mailto:s.booten@griffith.edu.au'), Target('_blank'), Rel('noopener noreferrer')], 'Steven Booten'),
                Script([], f'{jsScript}'), '<br><br>',
                
                
                H1([Id('top'), Class('title')], [f'Quality Assurance report for Course: {myCanvas.courseCode.replace("_"," ")}']),
                
                Div([Class('content')],
                        #Head([Class('message-header is-size-10')], 'Heuristics'),
                        #    Ul([],
                        #    Li([Class('is-size-7')], ['The side navigation is refined to necessary course links and are organised so mutual content is next to each other (ie. content and assessment).']),
                        #    Li([Class('is-size-7')], ['The modules are easy to follow and not overwhelming to scroll through.']),
                        #    Li([Class('is-size-7')], ['The page accurately presents content that is clear and easy to follow.']),
                        #    Li([Class('is-size-7')], ['The discussions has been set up correctly.']),
                        #    Li([Class('is-size-7')], ['The content is accessible to those using screen-readers.']),
                        #    Li([Class('is-size-7')], ['The library areas (Files, Pages, Studio) of the course site are organised and articulate of the content they hold ']),
                        #    Li([Class('is-size-7')], ['When viewed as a student, the student experience is as expected with clear wayfinding and links/LTIs working as intended.'])
                        #)    
                    ),
                    htmlModule,
                    htmlFileStructure,
                    htmlBBIssues,
                    htmlPlaceholders,
                ), 
            )
        ),
        Script([], 'bulmaCollapsible.attach()')
    )
    
    return html





