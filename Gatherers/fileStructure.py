def collectCourseFiles(myCanvas, canvasQa):
    
    ignoredFolders = ['qa info', 'css']
    
    fileCount = {}
    fileStructure = {}
    canvasQa['fileReference'] = {}
    
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
            if item.id in canvasQa['usedFiles']:
                fileInformation['used'] = True
            else:
                fileInformation['used'] = False
                canvasQa['issues']['File Structure']['unused'] = canvasQa['issues']['File Structure'].get('unused', 0) + 1
            
            #creating a simple dictionary of files and related folders for use in other checks.
            if canvasQa['fileReference'].get(item.filename, None) is None:
                canvasQa['fileReference'][item.filename] = {}  
                canvasQa['fileReference'][item.filename]['folders'] = []
            canvasQa['fileReference'][item.filename]['folders'].append({folderName : folderUrl})
            
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
                canvasQa['issues']['File Structure']['duplicate'] = canvasQa['issues']['File Structure'].get('duplicate', 0) + 1
    
    canvasQa['issues']['File Structure']['count'] = canvasQa['issues']['File Structure'].get('duplicate', 0)  + canvasQa['issues']['File Structure'].get('unused', 0)
             
    return fileStructure