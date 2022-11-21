from simple_settings import settings
from Checks.body import checkQuizBody
from pprint import pprint

def collectCourseAssignments(myCanvas):
    usedFiles = []
    assignmentGroups = myCanvas.getAssignmentGroups(['assignments'])
    assignmentInfo = {}
    for group in assignmentGroups:
        assignmentInfo[group.id] = assignmentInfo.get(group.name, {})
        assignmentInfo[group.id]['weight'] = group.group_weight
        assignmentInfo[group.id]['title'] = group.name
        assignmentInfo[group.id]['url'] = f'{settings.CANVAS_API_URL}/courses/{myCanvas.courseId}/assignments'
        assignmentInfo[group.id]['assignments'] = {}
        #pprint(group.assignments)
        for assignment in group.assignments:
            assignmentInfo[group.id]['assignments'][assignment['id']] = {}
            assignmentInfo[group.id]['assignments'][assignment['id']]['title'] = assignment['name']
            assignmentInfo[group.id]['assignments'][assignment['id']]['description'] = assignment['description']
            assignmentInfo[group.id]['assignments'][assignment['id']]['points'] = assignment['points_possible']
            assignmentInfo[group.id]['assignments'][assignment['id']]['due'] = assignment['due_at']
            assignmentInfo[group.id]['assignments'][assignment['id']]['published'] = assignment['published']
            assignmentInfo[group.id]['assignments'][assignment['id']]['submissionTypes'] = assignment['submission_types']
            assignmentInfo[group.id]['assignments'][assignment['id']]['url'] = assignment['html_url']
            
            if 'online_quiz' in assignment['submission_types']:
                assignmentInfo[group.id]['assignments'][assignment['id']]['quiz'], usedFilestemp = quizQa(myCanvas, assignment['quiz_id'])
            else:
                assignmentInfo[group.id]['assignments'][assignment['id']]['quiz'], usedFilestemp = None, []
            usedFiles += usedFilestemp
                
    return assignmentInfo, usedFiles

    
def quizQa(myCanvas, quizId):
    quiz = myCanvas.getQuiz(quizId)

    questionInfo = {}
    
    bbSearchTerm = '@X@EmbeddedFile.requestUrlStub@X@webapps' 
    

    for question in quiz.get_questions():
        questionInfo[question.id] = {}
        questionInfo[question.id]['title'] = question.question_name
        questionInfo[question.id]['questionType'] = question.question_type
        questionInfo[question.id]['points'] = question.points_possible
        questionInfo[question.id]['body'] = question.question_text if question.question_text is not None else ''
        questionInfo[question.id]['hasCorrectAnswer'] = hascorrectAnswer(question)
        questionInfo[question.id]['quizIssues'] = []
        questionInfo[question.id]['bbBrokenLinks'] = []
        
        
        if question.question_type == 'Hot Spot' or question.question_type == 'Quiz Bowl' or question.question_type == 'File Upload':
            questionInfo[question.id]['quizIssues'] = {question.question_type : "Incompatible Question from BB to Canvas"}
        if question.question_text.find('question text for this question was too long') > -1:
            questionInfo[question.id]['quizIssues'] = {question.question_type : "Question is too Long will need to be remade"}
        if question.question_type == 'Calculated Formula' or question.question_type == 'Calculated Numeric':
            questionInfo[question.id]['quizIssues'] = {question.question_type : "Question can't be edited"}
        
        if question.question_text.find(bbSearchTerm) > -1:
            questionInfo[question.id]['bbBrokenLinks'] = {'Question Text': "Broken embed inside Question Body"}
        if question.correct_comments_html is not None:
            if question.correct_comments_html.find(bbSearchTerm) > -1:
                questionInfo[question.id]['bbBrokenLinks'] += {'Correct Comment': "Broken embed inside Correct Comments"}
        if question.incorrect_comments_html is not None:
            if question.incorrect_comments_html.find(bbSearchTerm) > -1:
                questionInfo[question.id]['bbBrokenLinks'] += {'Incorrect Comments' : "Broken embed inside Incorrect Comments"}
    
    
    
    
    return checkQuizBody(questionInfo, myCanvas)

def hascorrectAnswer(question):
    if question.question_type in ['matching_question', 'essay_question']:
        return True
    
    answers = question.answers
    
    for answer in answers:
        if answer.get('weight', 0) == 100:
            return True
        
    return False
    
            
