def collectCourseFiles(myCanvas, usedFileIds):
    
    fileIssues = {}
    ignoredFolders = ['qa info', 'css']
    
    fileCount = {}
    fileStructure = {}
    
    for folder in myCanvas.getFileFolders():
        
        
        if folder.name.lower() in ignoredFolders:
            continue
        
        #- this removes 'course files' from the name to help with asthetics
        if len(folder.full_name) > 12:
            folderName = folder.full_name[12::]
        else:
            folderName = '/'
        
        #- this generates a URL to the location of the file as the file.url variable is to directly download the file.    
        if folderName == '/':
            folderUrl = f'http://lms.griffith.edu.au/courses/{myCanvas.courseId}/files/'
        else:    
            folderUrl = f'http://lms.griffith.edu.au/courses/{myCanvas.courseId}/files/folder{folderName}'
        
        
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
                fileIssues['unused'] = fileIssues.get('unused', 0) + 1
            
            #- tracks how many times a file shows up in the courses file structure to then be added to the placeholder at the end  
            fileCount[item.filename] = fileCount.get(item.filename, 0) + 1
            
            fileList.append(fileInformation)

        fileStructure[folderName] = {}
        fileStructure[folderName]['fileCount'] = folder.files_count
        fileStructure[folderName]['url'] = folderUrl
        fileStructure[folderName]['files'] = fileList
            
    #- this replaces the placeholder defined when cycling through the folder items if there are duplicates
    for folder, values in fileStructure.items():
        for file in values['files']:
            file['count'] = fileCount[file['name']]
            if file['count'] > 1:
                fileIssues['duplicate'] = fileIssues.get('duplicate', 0) + 1
                    
    return fileStructure, fileIssues