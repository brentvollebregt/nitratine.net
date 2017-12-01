import zipfile
import os

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