try:
    from simple_settings import settings
except:
    from lib.CanvasSettings import CanvasSettings
    settings = CanvasSettings()
from Checks.body import checkQuizBody, checkAssessmentBody
from pprint import pprint

def collectCourseAssignments(myCanvas, canvasQa):
    usedFiles = []
    assignmentGroups = myCanvas.getAssignmentGroups(['assignments'])
    canvasQa['assignments'] = {}
    for group in assignmentGroups:
        canvasQa['assignments'][group.id] = canvasQa['assignments'].get(group.name, {})
        canvasQa['assignments'][group.id]['weight'] = group.group_weight
        canvasQa['assignments'][group.id]['title'] = group.name
        canvasQa['assignments'][group.id]['url'] = f'{settings.CANVAS_API_URL}/courses/{myCanvas.courseId}/assignments'
        canvasQa['assignments'][group.id]['assignments'] = {}
        #pprint(group.assignments)
        for assignment in group.assignments:
            #pprint(assignment)
            canvasQa['assignments'][group.id]['assignments'][assignment['id']] = {}
            canvasQa['assignments'][group.id]['assignments'][assignment['id']]['title'] = assignment['name']
            canvasQa['assignments'][group.id]['assignments'][assignment['id']]['description'] = assignment['description']
            canvasQa['assignments'][group.id]['assignments'][assignment['id']]['points'] = assignment['points_possible']
            canvasQa['assignments'][group.id]['assignments'][assignment['id']]['due'] = assignment['due_at']
            canvasQa['assignments'][group.id]['assignments'][assignment['id']]['published'] = assignment['published']
            canvasQa['assignments'][group.id]['assignments'][assignment['id']]['submissionTypes'] = getAssignmentType(assignment['submission_types'], assignment.get('external_tool_tag_attributes', None))
            canvasQa['assignments'][group.id]['assignments'][assignment['id']]['rubric'] = assignment.get('rubric')
            canvasQa['assignments'][group.id]['assignments'][assignment['id']]['url'] = assignment['html_url']
            
            canvasQa['assignments'][group.id]['assignments'][assignment['id']]['quiz'] = None
            usedFiles += checkAssessmentBody(canvasQa['assignments'][group.id]['assignments'][assignment['id']], myCanvas, canvasQa)
            
            if 'online_quiz' in assignment['submission_types']:
                quiz = myCanvas.getQuiz(assignment['quiz_id'])
                canvasQa['assignments'][group.id]['assignments'][assignment['id']]['questionCount'] = quiz.question_count
                canvasQa['assignments'][group.id]['assignments'][assignment['id']]['quiz'], usedFilestemp = quizQa(myCanvas, quiz, canvasQa)
                
                usedFiles += usedFilestemp
                
    return usedFiles

def getAssignmentType(canvasSubmissionType, externalToolAttributes):
    for submissionType in canvasSubmissionType:
        
        if 'discussion_topic' in submissionType:
            return 'Discussion Topic'
        elif 'online_quiz' in submissionType:
            return 'Online Quiz'
        elif 'on_paper' in submissionType:
            return 'On Paper'
        elif 'online_text_entry' in submissionType:
            return 'Online Text Entry'
        elif 'online_url' in submissionType:
            return 'Online Url'
        elif 'online_upload' in submissionType:
            return 'Online Upload'
        elif 'media_recording' in submissionType:
            return 'Media Recording'
        elif 'student_annotation' in submissionType:
            return 'Student Annotation'
        elif 'none' in submissionType:
            return 'None'
        elif 'external_tool' in submissionType:
            if 'https://lti.risingsoftware.com/launch?app=auralia' in externalToolAttributes['url']:
                return 'Auralia'
            elif 'https://lti.risingsoftware.com/launch?app=musition' in externalToolAttributes['url']:
                return 'Musition'
            elif 'https://padlet.com/' in externalToolAttributes['url']:
                return 'Padlet'
            elif 'https://au-lti.bbcollab.com/lti' in externalToolAttributes['url']:
                return 'Collaborate'
            elif 'https://echo360.net.au/lti' in externalToolAttributes['url']:
                return 'Echo 360'
            elif 'https://v3.pebblepad.com.au/atlas/pebble' in externalToolAttributes['url']:
                return 'Pebblepad'
            elif 'https://www.edu-apps.org/' in externalToolAttributes['url']:
                return 'Student Support'
            elif 'https://api.turnitin.com/api' in externalToolAttributes['url']:
                return 'Turnitin LTI'
            else:
                return 'New External Tool'
            
        

    
def quizQa(myCanvas, quiz, canvasQa):
    

    questionInfo = {}
    
    #bbSearchTerm = '@X@EmbeddedFile.requestUrlStub@X@webapps' 

    for question in quiz.get_questions():
        
        
        
        questionInfo[question.id] = {}
        questionInfo[question.id]['title'] = question.question_name
        questionInfo[question.id]['questionType'] = question.question_type
        questionInfo[question.id]['points'] = question.points_possible
        questionInfo[question.id]['body'] = question.question_text if question.question_text is not None else ''
        questionInfo[question.id]['hasCorrectAnswer'] = hascorrectAnswer(question)
        questionInfo[question.id]['quizIssues'] = {}
        questionInfo[question.id]['bbBrokenLinks'] = {}
        
        
        if question.question_type == 'Hot Spot' or question.question_type == 'Quiz Bowl' or question.question_type == 'File Upload':
            questionInfo[question.id]['quizIssues'] = {question.question_type : "Incompatible Question from BB to Canvas"}
        if question.question_text.find('question text for this question was too long') > -1:
            questionInfo[question.id]['quizIssues'] = {question.question_type : "Question is too Long will need to be remade"}
        if question.question_type == 'Calculated Formula' or question.question_type == 'Calculated Numeric':
            questionInfo[question.id]['quizIssues'] = {question.question_type : "Question can't be edited"}
        
        #if question.question_text.find(bbSearchTerm) > -1:
        #    questionInfo[question.id]['bbBrokenLinks'] = {'Question Text': "Broken embed inside Question Body"}
        #if question.correct_comments_html is not None:
        #    if question.correct_comments_html.find(bbSearchTerm) > -1:
        #        questionInfo[question.id]['bbBrokenLinks'] = {'Correct Comment': "Broken embed inside Correct Comments"}
        #if question.incorrect_comments_html is not None:
        #    if question.incorrect_comments_html.find(bbSearchTerm) > -1:
        #        questionInfo[question.id]['bbBrokenLinks'] = {'Incorrect Comments' : "Broken embed inside Incorrect Comments"}
    
    return checkQuizBody(questionInfo, myCanvas, canvasQa)
        

def hascorrectAnswer(question):
    if question.question_type in ['matching_question', 'essay_question']:
        return True
    
    answers = question.answers
    
    for answer in answers:
        if answer.get('weight', 0) == 100:
            return True
        
    return False
    
            
