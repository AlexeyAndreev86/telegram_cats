from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError, FileNotUploadedError, FileNotDownloadableError

import constants
import os


class GoogleDiskAPI:
    __EXIST = None

    def __new__(cls, *args, **kwargs):
        if cls.__EXIST is None:
            cls.__EXIST = super().__new__(cls)
        return cls.__EXIST

    def __init__(self):
        self.auth = GoogleAuth()
        self.auth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.auth)
        self.folder = constants.GOOGLE_DRIVE_FOLDER_ID

    def upload(self, filename, path_to_file_for_upload):
        try:
            file_to_upload = self.drive.CreateFile({'title': filename, 'parents': [{'id': self.folder}]})
            file_to_upload.SetContentFile(path_to_file_for_upload)
            file_to_upload.Upload()
        except ApiRequestError as e:
            print(e)

    def download(self, file_id, file_name):
        try:
            drive = GoogleDrive(self.auth)
            file_to_download = drive.CreateFile({'id': file_id})
            file_to_download.GetContentFile(os.path.join(os.getcwd(), 'downloads', file_name))
        except (ApiRequestError, FileNotUploadedError, FileNotDownloadableError) as e:
            print(e)

    def get_content_list(self):
        file_list = self.drive.ListFile({'q': f"'{self.folder}' in parents and trashed=false"}).GetList()
        return [(file['title'], file['id']) for file in file_list]
