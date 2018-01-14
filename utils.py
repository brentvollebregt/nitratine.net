import zipfile
import os
import shutil

tmp_path = os.path.dirname(os.path.realpath(__file__)) + '/tmp/'

def createTmp():
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

def removeTmp():
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)

def zipFolder(location, filename):
    try:
        createTmp()
        path = tmp_path + filename
        zipf = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(location):
            for file in files:
                new_name = os.path.join(root, file).replace(location, '')
                zipf.write(os.path.join(root, file), new_name)
    except Exception as e:
        filename = False
        print (e)
    finally:
        zipf.close()

def unzipFolder(location):
    file = os.getcwd() + '/zip.zip'
    if os.path.exists(location):
        shutil.rmtree(location)
    os.makedirs(location)
    zip_ref = zipfile.ZipFile(file, 'r')
    zip_ref.extractall(location)
    zip_ref.close()
    os.remove(file)

def deleteFolder(location):
    if os.path.exists(location):
        shutil.rmtree(location)

def moveFolder(location_from, location_to):
    if os.path.exists(location_from):
        shutil.move(location_from, location_to)