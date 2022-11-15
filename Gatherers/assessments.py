def assignmentGroupQa(qaInfo):
    groups = qaInfo.course.getAssignmentGroups()
    assignmentlist = []
    for group in groups:
        assignments = qaInfo.course.getGroupAssignments(group)
        count = 0
        assignmentlist = []
        for assignment in assignments:
            count +=1 
            submission = ''
            for item in assignment.submission_types:
                submission += f'{item} '
            assignmentlist.append([assignment.name, assignment.html_url, assignment.points_possible, submission.replace('_', ' '), assignment.published])
        if qaInfo.assignmentGroups.get(group.name, None) == None:
            qaInfo.assignmentGroups[group.name] = []
        qaInfo.assignmentGroups[group.name].append([group.group_weight, count, assignmentlist])
        qaInfo.assessmentGroupSum += group.group_weight
        
        
def quizQA(qaInfo, browser):
    quizzes = qaInfo.course.getQuizzes()
    
    
    
    
    
    search = '@X@EmbeddedFile.requestUrlStub@X@webapps' 
    
    for quiz in quizzes:
        questions = qaInfo.course.getQuizQuestions(quiz)
        for question in questions:
            body = question.question_text
            
            imageTags = qaInfo.course.getPageImgTags(body)
            if len(imageTags) > 0:
                if qaInfo.imgTags.get(quiz.title, None) == None:
                    qaInfo.imgTags[quiz.title] = []
                imgLinkCheck(browser, qaInfo, imageTags, quiz.title, quiz.html_url, quizpage=True)
                
                for key, link in imageTags.items():
                    try:
                        link.index('lms.griffith.edu.au/courses/')
                        index = link.index('=')
                        try:
                            end = link[index:].index('&')
                            end += index
                        except:
                            end = len(link)
                            pass
                        id = link[index+1:end]
                        if qaInfo.usedFilesId.get(id, None) == None:
                            qaInfo.usedFilesId[id] = []
                        qaInfo.usedFilesId[id].append(question)
                    except:
                        pass       
                    
            links = qaInfo.course.getPageLinks(body)
            for link in links:
                linkCheck(browser, qaInfo, link, quiz.title, quiz.html_url, question, quizpage=True)
                
                
            if question.question_type == 'Hot Spot' or question.question_type == 'Quiz Bowl' or question.question_type == 'File Upload':
                if qaInfo.quizQa.get('Incompatible Question Type', None) is None:
                    qaInfo.quizQa['Incompatible Question Type'] = []
                qaInfo.quizQa['Incompatible Question Type'].append([quiz.title, quiz.html_url, question.question_name, question.question_type, "Incompatible Question from BB to Canvas"])
            if question.question_text.find('question text for this question was too long') > 0:
                if qaInfo.quizQa.get('Question Too Long', None) is None:
                    qaInfo.quizQa['Question Too Long'] = []
                qaInfo.quizQa['Question Too Long'].append([quiz.title, quiz.html_url, question.question_name, question.question_type, "Question is too Long will need to be remade"])
            if question.question_type == 'Calculated Formula' or question.question_type == 'Calculated Numeric':
                if qaInfo.quizQa.get("Math's Question", None) is None:
                    qaInfo.quizQa["Math's Question"] = []
                qaInfo.quizQa["Math's Question"].append([quiz.title, quiz.html_url, question.question_name, question.question_type, "Can't be edited"])
            try:    
                if question.question_text.find(search) > -1:
                    if qaInfo.quizQa.get('Broken embed from BB import', None) is None:
                        qaInfo.quizQa['Broken embed from BB import'] = []
                    qaInfo.quizQa['Broken embed from BB import'].append([quiz.title, quiz.html_url, question.question_name, question.question_type, "Broken embed inside Question Body"])
            except:
                try:
                    if question.correct_comments_html.find(search) > 0:
                        if qaInfo.quizQa.get('Broken embed from BB import', None) is None:
                            qaInfo.quizQa['Broken embed from BB import'] = []
                        qaInfo.quizQa['Broken embed from BB import'].append([quiz.title, quiz.html_url, question.question_name, question.question_type, "Broken embed inside Correct Comments"])
                except:
                    try:
                        if question.incorrect_comments_html.find(search) > 0:
                            if qaInfo.quizQa.get('Broken embed from BB import', None) is None:
                                qaInfo.quizQa['Broken embed from BB import'] = []
                            qaInfo.quizQa['Broken embed from BB import'].append([quiz.title, quiz.html_url, question.question_name, question.question_type, "Broken embed inside Incorrect Comments"])
                    except:
                        pass
                    
            if question.question_type == 'matching_question':
                continue
            
            answers = question.answers
            hasNoCorrect = False
            
            for answer in answers:
                if answer.get('weight', 0) == 100:
                    hasNoCorrect = False
                    break
                else:
                    hasNoCorrect = True
            if hasNoCorrect:
                if qaInfo.quizQa.get('No Correct Answer Found', None) is None:
                    qaInfo.quizQa['No Correct Answer Found'] = []
                qaInfo.quizQa['No Correct Answer Found'].append([quiz.title, quiz.html_url, question.question_name, question.question_type, "This question doesn't have a defined correct answer."])
                    
    return qaInfo