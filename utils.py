import zipfile
import os
import shutil

def zipArticle(article_location, sub, url):
    # TODO Checks for old zip files (delete)
    try:
        filename = 'articleZip_' + sub + '_' + url + '.zip'
        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(os.path.join(article_location + sub + '/' + url + '/')):
            for file in files:
                zipf.write(os.path.join(root, file))
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

def moveZip(article_location, sub, url):
    folder = article_location + sub + "/" + url + "/"
    file = os.getcwd() + '\\zip.zip'
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    zip_ref = zipfile.ZipFile(file, 'r')
    zip_ref.extractall(folder)
    zip_ref.close()
    os.remove(file)
