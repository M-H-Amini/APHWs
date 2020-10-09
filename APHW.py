import zipfile
import os
import shutil
import re

hw_zipfile = 'APHW1.zip'

temp_dest = 'temp'
submission_dest = 'aphw'
moss_dest = 'moss'

if not os.path.isdir(temp_dest):
    os.mkdir(temp_dest)
if not os.path.isdir(submission_dest):
    os.mkdir(submission_dest)
if not os.path.isdir(moss_dest):
    os.mkdir(moss_dest)


formats = ['.cpp', '.h', '.py', '.hpp', '.pdf']
desired_filenames = ['aphw1.cpp', 'aphw1.h']


def extractZip(zip_path, dest):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(dest, zip_path[:-4]))
        files = zip_ref.namelist()
    return files

zip_path = 'SeyedAliGhaziAsgar9623705.zip'

def processStudent(zip_path):
    r1 = re.compile('([a-zA-Z]*)[\W]*([0-9]*)')
    pr1 = r1.match(os.path.basename(os.path.basename(zip_path)))
    if pr1:
        student_name = pr1.group(1)
        student_id = pr1.group(2)

    name_flag = True if (len(student_id) and len(student_name)) else False

    if not len(student_id):
        student_id = os.path.basename(zip_path)

    files = extractZip(zip_path, temp_dest)
    student_path = os.path.join(temp_dest, zip_path[:-4])
    ##  All files of the desired formats in the submission
    existing_files = {key:[i for i in files if i.endswith(key)] for key in formats}
    ##  Files with correct name and format in the submission
    ok_files = [f for f in files for name in desired_filenames if f.endswith(name)]
    ok_files.extend(existing_files['.pdf'])
    ok_files = [os.path.join(temp_dest, zip_path[:-4], f) for f in ok_files]

    if not os.path.isdir(os.path.join(submission_dest, os.path.basename(zip_path)[:-4])):
        os.mkdir(os.path.join(submission_dest, os.path.basename(zip_path)[:-4]))
    
    student_dest = os.path.join(submission_dest, os.path.basename(zip_path)[:-4])

    for file in ok_files:
        shutil.copy2(file, student_dest)
        if not (file.endswith('.pdf') or file.endswith('.h')):
            shutil.copy2(file, os.path.join(moss_dest, student_id + os.path.basename(file)))
    
    files_flag = True if len(ok_files)==len(desired_filenames) + 1 else False

    if files_flag:
        shutil.rmtree(os.path.join(temp_dest, zip_path[:-4]))
        

    flags = {'name':name_flag, 'files':files_flag}
    properties = student_id, student_name

    return existing_files, ok_files, flags, properties

##  Extracts the big zipfile and processes each student with processStudent
def extractHW(hw_zipfile):
    extractZip(hw_zipfile, '.')
    student_folders = os.listdir(hw_zipfile[:-4])
    faults = []
    for sf in student_folders:
        student_persian_name = sf.split('_')[0]
        zip_paths = os.listdir(os.path.join(hw_zipfile[:-4], sf))
        zip_path = os.path.join(hw_zipfile[:-4], sf, zip_paths[0])
        ex, ok, flags, props = processStudent(zip_path)
        if not (flags['name'] and flags['files']):
            faults.append([props, flags, student_persian_name])
    shutil.rmtree(temp_dest)
    return faults

def getStudentNames(folder):
    return os.listdir(folder)

#print(extractHW(hw_zipfile))
print(getStudentNames('aphw'))