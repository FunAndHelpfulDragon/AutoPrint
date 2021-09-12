import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

# Google API Class:
#
# Class Call ("GoogleApi()")
# - setups script
# - Required inputs
#   - folder id of files
#   - folder id of where to move files once done
#   - path of where to store tempary downloaded files
#
# GetFilesForDownload()
# - goes through folder id (not move) and makes a list of Files
#
# DownloadFiles()
# - Download files stored from the list generated in GetFilesForDownload
#
# Move Files()
# - Moves files from stored folder id to move folder id
#
# list()
# - prints out a list for all files in a folder (and their id)


class GoogleApi:

    def __init__(self, folder_Id, move_Folder_Id, path):
        self.service = self.__LoadAPI__()
        self.folder_id = folder_Id
        self.moveFolder_Id = move_Folder_Id
        self.Path = path

    def __LoadAPI__(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('drive', 'v3', credentials=creds)

    def GetFilesForDownload(self):
        self.Files = []
        page_token = None

        while True:
            print(self.folder_id)
            response = self.service.files().list(
                q=f"mimeType='image/png' and parents in '{self.folder_id}'",
                spaces='drive',
                fields='nextPageToken, files(id, name)',
                pageToken=page_token).execute()

            for file in response.get('files', []):
                self.Files.append(file)

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    def DownloadFiles(self):
        self.GetFilesForDownload()
        print("-------------------Downloading Files----------------------")
        self.newFiles = []
        for file in self.Files:
            file_Id = file.get('id')
            print(f"{file.get('name')} ({file.get('id')})")

            # download stuff
            request = self.service.files().get_media(fileId=file_Id)  # noqa
            fileHandler = io.BytesIO()
            downloader = MediaIoBaseDownload(fileHandler, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Downloaded {int(status.progress()) * 100}%")
            html = fileHandler.getvalue()

            with open(f"{self.Path}{file.get('name')}", 'wb') as f:
                f.write(html)
                self.newFiles.append(f)
        print("----------------------------END---------------------------")

    def MoveFiles(self):
        print("Moving Files")
        self.GetFilesForDownload()  # make sure it has files
        for file in self.Files:
            file_Id = file.get('id')
            currentfile = self.service.files().get(fileId=file_Id,
                                                   fields='parents').execute()
            previousParent = ",".join(currentfile.get('parents'))
            self.service.files().update(fileId=file_Id,
                                        addParents=self.moveFolder_Id,
                                        removeParents=previousParent,
                                        fields='id, parents').execute()
            print(f"Moved file: {file.get('name')} to {self.moveFolder_Id}")

    def List(self):
        print("----------------------Files in Drive----------------------")
        self.GetFilesForDownload()
        for file in self.Files:
            print(f"{file.get('name')} ({file.get('id')})")
        print("----------------------------END---------------------------")

# ComputerApi class
#
# Class Call("ComputerApi()")
# - makes a folder called "ToPrint" for tempary download storage
#
# DeleteFile()
# - deletes a file, requires path of file
#
# DeleteAll()
# - deletes all files in the ToPrint folder
#
# GetFiles()
# - get files in the ToPrint folder
#
# PrintFiles()
# - sends the file to the printer


class ComputerApi:

    def __init__(self):
        if not os.path.exists("ToPrint"):
            os.mkdir("ToPrint")
            print("Made directory")
        self.Path = "ToPrint/"
        if not os.path.exists("Pdf"):
            os.mkdir("Pdf")
            print("Made directory")

    def DeleteFile(self, file_Path):
        os.remove(file_Path)

    def DeleteAll(self):
        self.GetFiles()
        for file in self.files:
            self.DeleteFile(file)

    def GetFiles(self):
        print("Getting files")
        files = []
        for file in os.listdir("ToPrint"):
            files.append("ToPrint/" + file)
        self.files = files

    def PrintFiles(self, printer, file_to_print):
        print(file_to_print)
        print(printer)
        print("Printing files")
        if printer != " ":
            os.system(f"lp -d {printer} {file_to_print}")
        else:
            os.system(f"lp {file_to_print}")

    def GenerateFile(self):
        print("-----------------------Generating File--------------------")
        self.GetFiles()
        i = 0
        length = len(self.files)
        if length > 0:
            print("Making pdf")
            # do we need to do this?
            if (length % 2) != 0:
                self.files = self.files[:-1]  # removes one from the array to make even.  # noqa

            for image in self.files:
                i = i + 1
                img = Image.open(image)
                img = img.rotate(90, expand=True)
                img.thumbnail((570, 820), Image.ANTIALIAS)
                # img.save(img, "JPEG")

                # img = Image.open(image)
                imgN = Image.new('RGB',
                                 (595, 842),  # a4 size
                                 (255, 255, 255))  # white background
                imgN.paste(img, (10, 10))
                imgN.save(f"Pdf/PDFTest{i}", 'PDF', quality=100)

            # merges the pdf's generted above into 1
            mergedObj = PdfFileMerger()
            for pdfFile in os.listdir("Pdf"):
                if pdfFile != ".DS_Store":
                    mergedObj.append(PdfFileReader(f"Pdf/{pdfFile}", 'rb'))
            mergedObj.write("yourfile.pdf")

            print(f"Output: {os.path.dirname(__file__)}/yourfile.pdf")
        else:
            print("WARNING: no images downloaded!")

        print("----------------------------END---------------------------")

    def CleanUp(self):
        print("-------------------Cleaning up other files---------------")
        # removes temp files
        for file in os.listdir("Pdf"):
            os.remove("Pdf/" + file)
        for file in os.listdir("ToPrint"):
            os.remove("ToPrint/" + file)
        try:
            os.remove("yourfile.pdf")
        except FileNotFoundError:
            print("File not found: yourfile.pdf")

        print("----------------------------END---------------------------")
