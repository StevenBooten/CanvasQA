def fileQA(myCanvas, usedFileIds):
    
    ignoredFolders = ['QA Info', 'css']
    
    fileCount = {}
    
    for folder in myCanvas.getFileFolders():
        
        fileStructure = {}
        if folder.name.lower() in ignoredFolders:
            continue
        
        #- this removes 'course files' from the name to help with asthetics
        if len(folder.full_name) > 12:
            folderName = folder.full_name[12::]
        else:
            folderName = '/'
        
        #- this generates a URL to the location of the file as the file.url variable is to directly download the file.    
        if folderName == '/':
            folderUrl = f'http://lms.griffith.edu.au/courses/{qaInfo.course.courseId}/files/'
        else:    
            folderUrl = f'http://lms.griffith.edu.au/courses/{qaInfo.course.courseId}/files/folder{folderName}'
        
        
        fileList = []
        for item in folder.get_files():
            fileInformation = {}
            fileInformation['name'] = item.filename
            fileInformation['id'] = item.id
            fileInformation['url'] = f'{folderUrl}?preview={item.id}'
            fileInformation['count'] = 0
            if item.id in usedFileIds:
                fileInformation['used'] = True
            else:
                fileInformation['used'] = False
            
            #- tracks how many times a file shows up in the courses file structure to then be added to the placeholder at the end  
            fileCount[item.id] = fileCount.get(item.id, 0) + 1
            
            fileList.append(fileInformation)

        fileStructure[folderName] = {}
        fileStructure[folderName]['fileCount'] = folder.files_count
        fileStructure[folderName]['files'] = fileList
            
    #- this replaces the placeholder defined when cycling through the folder items if there are duplicates
    for key, value in fileStructure.items():
        for x in value['files']:
            if fileCount.get(x['id'], 0) > 1:
                x['count'] = fileCount[x['id']]
                    
    return fileStructure