from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

auth = GoogleAuth()
auth.LocalWebserverAuth()
drive = GoogleDrive(auth)
images_folder = '1G66jpbXYwpxPKdeLmWY10ndnJPzup4TX'

def upload(filename, path):
    try:
        drive = GoogleDrive(auth)
        file_to_upload = drive.CreateFile({'title': filename})
        file_to_upload.SetContentFile(path)
        file_to_upload.Upload()
    except Exception as e:
        print(e)


def download():
    drive = GoogleDrive(auth)
    file_to_download = drive.CreateFile({'id': file5['id']})

    pass


def main():
    # upload('cat.jpg', r'C:\Users\user\Downloads\cat.jpg')
    # fileList = drive.ListFile().GetList()
    fileList = drive.ListFile({'q': f"'{images_folder}' in parents and trashed=false"}).GetList()
    print(fileList)
    print(len(fileList))
    for file in fileList:
        print('Title: %s, ID: %s' % (file['title'], file['id']))



if __name__ == '__main__':
    main()
