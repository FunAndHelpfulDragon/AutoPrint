import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from google.auth.exceptions import RefreshError
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader
import datetime
import webhookTest as web
import shutil

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
#
# MakeFolder()
# - Makes a sub folder under the folder they want to move to with the time of creation as the name  # noqa


class GoogleApi:

    def __init__(self, folder_Id, move_Folder_Id, path):
        self.service = self.__LoadAPI__()
        self.folder_id = folder_Id
        self.moveFolder_Id = move_Folder_Id
        self.Path = path

    def __LoadAPI__(self):
        try:
            creds = None
            if os.path.exists(f'{os.path.dirname(__file__)}/token.json'):
                creds = Credentials.from_authorized_user_file(f'{os.path.dirname(__file__)}/token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        f'{os.path.dirname(__file__)}/credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(f'{os.path.dirname(__file__)}/token.json', 'w') as token:
                    token.write(creds.to_json())

            return build('drive', 'v3', credentials=creds)
        except RefreshError:
            os.remove(f"{os.path.dirname(__file__)}/token.json")
            web.webhook().SendMessage("<@!467718535897022479> Google api authentication required")
            return self.__LoadAPI__()

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
        # self.GetFilesForDownload()  # make sure it has files
        if len(self.Files) == 0:
            self.GetFilesForDownload()
        self.newid = self.MakeFolder()
        for file in self.Files:
            file_Id = file.get('id')
            currentfile = self.service.files().get(fileId=file_Id,
                                                   fields='parents').execute()
            previousParent = ",".join(currentfile.get('parents'))
            self.service.files().update(fileId=file_Id,
                                        addParents=self.newid,
                                        removeParents=previousParent,
                                        fields='id, parents').execute()
            print(f"Moved file: {file.get('name')} to {id}")

    def MoveFilesBack(self):
        print("Moving files back")
        self.GetFilesForDownload()
        for file in self.files:
            file_Id = file.get('id')
            self.service.files().update(fileId=file_Id,
                                        addParents=self.moveFolder_Id,
                                        removeParents=self.newid,
                                        fields='id, parents').execute()
            print(f"Moved file: {file.get('name')} back to {self.moveFolder_Id}")  # noqa

    def List(self):
        print("----------------------Files in Drive----------------------")
        self.GetFilesForDownload()
        for file in self.Files:
            print(f"{file.get('name')} ({file.get('id')})")
        print("----------------------------END---------------------------")

    def MakeFolder(self):
        file_metadata = {
            'name': f'{datetime.datetime.now()}',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.moveFolder_Id]
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id').execute()
        return file.get('id')


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
        if not os.path.exists(f"{os.path.dirname(__file__)}/ToPrint"):
            os.mkdir(f"{os.path.dirname(__file__)}/ToPrint")
            print("Made ToPrint directory")
        self.Path = f"{os.path.dirname(__file__)}/ToPrint/"
        if not os.path.exists(f"{os.path.dirname(__file__)}/Pdf"):
            os.mkdir(f"{os.path.dirname(__file__)}/Pdf")
            print("Made Pdf directory")
        if not os.path.exists(f"{os.path.dirname(__file__)}/tmp"):
            os.mkdir(f"{os.path.dirname(__file__)}/tmp")
            print("Made tmp directory")

    def DeleteFile(self, file_Path):
        os.remove(file_Path)

    def DeleteAll(self):
        self.GetFiles()
        for file in self.files:
            self.DeleteFile(file)

    def GetFiles(self):
        print("Getting files")
        files = []
        for file in os.listdir(f"{os.path.dirname(__file__)}/ToPrint"):
            files.append(f"{os.path.dirname(__file__)}/ToPrint/" + file)
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
                if image != f"{os.path.dirname(__file__)}/ToPrint/.DS_Store":
                    # imageHeight = 2560
                    # Resolution in DPI, assumes input image is 2560 on long size.
                    # resolution = imageHeight / (29.7 * 0.397008)
                    # imageWidth = int(resolution * (21.0 * 0.397008))
                    # resolution = int(resolution)

                    imageHeight = 842
                    imageWidth = 595

                    i = i + 1
                    img = Image.open(image)
                    img = img.convert('RGB')
                    img = img.rotate(90, expand=True)
                    print(imageWidth)
                    print(imageHeight)
                    img.thumbnail((imageWidth - 20, imageHeight - 20), Image.ANTIALIAS)
                    img.save(f"{os.path.dirname(__file__)}/tmp/img{i}.png")

                    import img2pdf
                    a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
                    layout_fun = img2pdf.get_layout_fun(a4inpt)
                    with open(f"{os.path.dirname(__file__)}/Pdf/PDFTest{i}.pdf", "wb") as f:
                    	f.write(img2pdf.convert(f"{os.path.dirname(__file__)}/tmp/img{i}.png", layout_fun=layout_fun))

                    # imgN = Image.new('RGB',
                    #                  (imageWidth, imageHeight),  # a4 size
                    #                  (255, 255, 255))  # white background
                    # imgN.paste(img, img.getbbox())#(10, 10))
                    # imgN.save(f"{os.path.dirname(__file__)}/Pdf/PDFTest{i}.pdf", quality=50)

            # merges the pdf's generted above into 1
            mergedObj = PdfFileMerger()
            for pdfFile in os.listdir(f"{os.path.dirname(__file__)}/Pdf"):
                if pdfFile != ".DS_Store":
                    mergedObj.append(PdfFileReader(f"{os.path.dirname(__file__)}/Pdf/{pdfFile}", 'rb'))
            mergedObj.write(f"{os.path.dirname(__file__)}/yourfile.pdf")

            web.webhook().SendMessage(f"Output: {os.path.dirname(__file__)}/yourfile.pdf")
            print(f"Output: {os.path.dirname(__file__)}/yourfile.pdf")

        else:
            print("WARNING: no images downloaded!")

        print("----------------------------END---------------------------")

    def CleanUp(self):
        print("-------------------Cleaning up other files---------------")
        # removes temp files
        for file in os.listdir(f"{os.path.dirname(__file__)}/Pdf"):
            os.remove(f"{os.path.dirname(__file__)}/Pdf/" + file)
        for file in os.listdir(f"{os.path.dirname(__file__)}/tmp"):
            os.remove(f"{os.path.dirname(__file__)}/tmp/" + file)
        if input("Remove downloaded files? (y = yes): ").lower() == "y":
            for file in os.listdir(f"{os.path.dirname(__file__)}/ToPrint"):
                os.remove(f"{os.path.dirname(__file__)}/ToPrint/" + file)
        try:
            os.remove(f"{os.path.dirname(__file__)}/yourfile.pdf")
        except FileNotFoundError:
            print("File not found: yourfile.pdf")

        print("----------------------------END---------------------------")

    def TestFile(self):
        blankimg = f"{os.path.dirname(__file__)}/Blank.png"
        for x in range(0, 8):
            shutil.copy2(blankimg, os.path.join(f"{os.path.dirname(__file__)}/ToPrint/", f"Blank({x})"))
