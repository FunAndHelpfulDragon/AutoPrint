# Installation

1. Clone / Download this repostratry
2. Download python

RECOMMENDATION: do this in a virtual enviroment, https://docs.python.org/3/tutorial/venv.html. This means you can download any python modules without needing adminstrator permission.

3. install these modules (copy and past):
    `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
    `pip install pillow`
    `pip install PyPDF2`
4. Download `Test1.png` and run `lp Test1.png` (Test1.png is a blank image (transparent), so it shouldn't waste any ink)
   - This program uses CUPS to print out the file, by doing this you are checking that you can print out a file
   - If this doesn't work install CUPS: http://www.cups.org/ (it might be different depending on the os)
   - Also try doing `lp -d {Printer Name} Test1.png` if the default printer is not the printer you want.
   - NOTE: Change the default double sided print settings to long-edge, this will just save paper when printing multiple images. If you don't want this to happen then leave it on normal. Change the default settings can be done here: http://127.0.0.1:631/ (this is local to YOUR computer so it would not effect any other device.).
     - If you don't change it, nothing bad would happen. If you downloaded 7 files, only 6 will print. (but all 7 will get moved)
5. Follow these documentations to get the google api to work:
   - https://developers.google.com/workspace/guides/create-project
   - https://developers.google.com/workspace/guides/create-credentials
   - (if needed): https://developers.google.com/drive/api/v3/quickstart/python#step_3_run_the_sample
6. Give your google account permission to access the drive. (if it asks about if you are sure you want to continue, click continue as you created it.)
7. Everything is setup, use the Text based interface to print files.

# To run
run `python Main.py` in the virtual enviroment (if set up) or just normally
