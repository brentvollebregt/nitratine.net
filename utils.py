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

def zipArticle(article_location, sub, article):
    try:
        createTmp()
        filename = 'articleZip_' + sub + '_' + article + '.zip'
        path = tmp_path + filename
        zipf = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(os.path.join(article_location + sub + '/' + article + '/')):
            for file in files:
                new_name = os.path.join(root, file).replace(os.path.join(article_location + sub + '/' + article + '/'), '')
                zipf.write(os.path.join(root, file), new_name)
    except Exception as e:
        filename = False
        print (e)
    finally:
        zipf.close()
    return filename

def deleteArticleFiles(article_location, sub, url):
    folder = article_location + sub + "/" + url + "/"
    if os.path.exists(folder):
        shutil.rmtree(folder)

def unzipArticle(article_location, sub, url):
    folder = article_location + sub + "/" + url + "/"
    file = os.getcwd() + '/zip.zip'
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    zip_ref = zipfile.ZipFile(file, 'r')
    zip_ref.extractall(folder)
    zip_ref.close()
    os.remove(file)

def zipArticleFolder(location):
    try:
        createTmp()
        filename = 'ArticleFolder.zip'
        path = tmp_path + filename
        zipf = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(location):
            for file in files:
                new_name = os.path.join(root, file).replace(location, '')
                zipf.write(os.path.join(root, file), new_name)
    except Exception as e:
        filename = False
        print(e)
    finally:
        zipf.close()
    return filename

def unzipArticleFolder(location):
    file = os.getcwd() + '/zip.zip'
    if os.path.exists(location):
        shutil.rmtree(location)
    os.makedirs(location)
    zip_ref = zipfile.ZipFile(file, 'r')
    zip_ref.extractall(location)
    zip_ref.close()
    os.remove(file)
