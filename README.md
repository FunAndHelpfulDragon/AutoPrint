# Description
This python program is designed for downloading and printing off files from google drive. Using the google drive API a whole bunch of settings, you can print anything in any folder (you need to give it the folder id) and then move them to another folder

# REQUIREMENTS
- python 3

# Installation
1. Clone / Download this repostratry

RECOMMENDATION: Do this in a virtual enviroment, https://docs.python.org/3/tutorial/venv.html. This means you can download any python modules without needing adminstrator permission.

3. install these modules (copy and past):
    `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
    `pip install pillow`
    `pip install PyPDF2`
    `pip install pygame`  (not needed if running headless mode (without UI))
    NOTE: you might need to run `sudo apt-get install python3-sdl2` if the program isn't working.

4. Set up the printer
   - Make sure CUPS is installed, you can test this by running `lp {Path To Folder}\Blank.png` this should print a transparent page out.
   - If CUPS is not installed, install it via http://www.cups.org/

   - Recommendations:
   - Make the printer default to 2 sided, This will save paper in the long run.
   - Set the printer quality to a higher level than the normal level, This will make the images look better
   - Set the printer to the default printer for that device. (you don't have to, but it's easier when running the program)

5. Follow these documentations to get the google api to work (Sorry, google api can be annoying sometimes, and it's just easier to do it this way):
   - https://developers.google.com/workspace/guides/create-project
   - https://developers.google.com/workspace/guides/create-credentials
   - (if needed): https://developers.google.com/drive/api/v3/quickstart/python#step_3_run_the_sample

6. Make sure your google account has access to the 2 folders that you want to use.
7. Everything is setup, use the Text/UI based interface to print files.

# To run
run `python Program.py` in the virtual enviroment (if set up) or just normally.
when asked for google drive folder id, paste in the id. To get the id, go to that folder and in the URL copy the last string of the folder.
when asked for the printer, leave it blank to use the default printer (for that device) else put in the printer name.
when asked to deleted files after use, Recommendation is yes those are just temparay files that have been downloaded, the program doesn't need them any more. (no is an option, but then they will be included in the next pdf.

# Notes
- Fell free to edit the repostratry and do a pull request, This Program was made in about a week.
