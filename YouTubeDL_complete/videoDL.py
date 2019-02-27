#--------------------------------------------------------------------
# TITLE: Internet Video Downloader 
# AUTHOR: Andre Rosa
# DATE: 18 FEB 2018
# TESTED WITH: Youtube, Twitch, Daily Motion, Facebook, Veoh and Liveleak
# OBJECTIVE: This module is the FIRST part of the Categorizer Program. 
#--------------------------------------------------------------------

# PROBLEM:
# Some files are downloaded as mkv, flv and other formats. The program failed when converting some of these files to mp4.
# I tried to convert from mkv to h.264 and got an error of a missing codec, check available codecs with 'ffmpeg -codecs'
# look some explanation on: https://stackoverflow.com/questions/30898671/converting-mkv-to-h-264-ffmpeg
# and then on: https://askubuntu.com/questions/483187/winff-ffmpeg-unknown-encoder-libvo-aacenc
# The problem is that some codecs that allow conversion are missing on this computer. 
# I will not install the missing codecs because the final user will not use this computer for production.
# SOLUTION:
# if the program can not convert the video to mp4 it will ignore the video and add a line in the Error_Report 'missing codec to convert to mp4'

# DEPENDENCIES
from __future__ import unicode_literals

import youtube_dl   # version 2019.2.8   https://anaconda.org/conda-forge/youtube-dl
                    # for a list of supported sites for youtube_dl: https://rg3.github.io/youtube-dl/supportedsites.html
import urllib       # version 1.7.1      https://anaconda.org/conda-forge/python_http_client

# mylibs
# import sys
# sys.path.insert(0, '../../0. Commons')
from sysColor import sysColor

#=========================================================================================
# VIDEODOWNLOADER
#=========================================================================================
class VideoDownloader:

    #=========================================================
    # VIDEO INFO: Nested class holds the information about a video
    #=========================================================
    class VideoInfo:
        def __init__(self, info, url, uniqueName):
            ''' VideoInfo Constructor '''
            self.vid_url = url
            self.vid_id = info.get("id", None)
            self.vid_uname = uniqueName # generates a unique name for the video
            self.vid_title = info.get('title', None) # the original video title taken from the home page
            self.vid_vcodec = info.get('vcodec', None) #video codec
            self.vid_acodec = info.get('acodec', None) #audio codec

        # Return a message about the codecs for the video
        def getCodedInfo (self):
            ''' Return a text message about the video to be saved on file. '''
            msg = str(str(self.vid_uname) + ',' + str(self.vid_vcodec) + ',' + str(self.vid_acodec) + ',' +  str(self.vid_url) )
            return msg
        
        def getVideoName (self):
            ''' Return the string Video Title '''
            return self.vid_uname
    #=========================================================

    #=========================================================
    # NESTED CLASS USED TO AVOID TOO VERBOSE YOUTUBE_DL MESSAGES
    #=========================================================
    class MyLogger:
        def debug(self, msg):
            pass
        def warning(self, msg):
            pass
        def error(self, msg):
            pass
            #print(msg)
    #=========================================================

    #------------------------------------------------------------
    def __my_hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
    #------------------------------------------------------------
    #------------------------------------------------------------
    def setVideoFolder(self, folder):
        self.videoFolder = folder
    #------------------------------------------------------------

    #------------------------------------------------------------
    # GENERATE A UNIVERSLLY UNIQUE IDENTIFIER FOR THE VIDEO NAME
    #------------------------------------------------------------
    def __generateUniqueName (self):
        ''' Return a universally unique identifier created with uuid.'''
        import uuid # https://docs.python.org/2/library/uuid.html
        return uuid.uuid4().hex # to create unique file names
    #------------------------------------------------------------

    #-------------------------------------------------------------
    # CONFIGURATION OF THE YOUTUBE DOWNLOADER
    #-------------------------------------------------------------
    def __getDLConfiguration(self, uniqueName):
        ''' Return the parameters used to download files with YouTube_DL '''

        # PARAMETERS FOR THE DOWNLOADER
        # https://github.com/rg3/youtube-dl/blob/master/README.md
        # https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
        ydl_opts = {
            'write-auto-sub': False,
            'skip-download': True,
            'recode-video': 'mp4',
            'outtmpl': self.videoFolder + '/' +  uniqueName + '.%(ext)s',   #'./videos/%(title)s.%(ext)s'
            'logger': self.logger,
            'progress_hooks': [self.__my_hook],
        } # https://stackoverflow.com/questions/35643757/how-to-set-directory-in-ydl-opts-in-using-youtube-dl-in-python

        return ydl_opts
    #---------------------------------------------------------------

    #---------------------------------------------------------------
    # VIDEODOWNLOADER CONSTRUCTOR
    #---------------------------------------------------------------
    def __init__(self, videoList = None):
        '''VideoDownloader Constructor receives the txt file (videoList) with the list of url to download.\n
        If no list is passed the downloader can be used to download single videos with download method '''

        if (videoList != None):
            self.files = self.__load_list (videoList)
            self.fileName = videoList
        else:
            self.files = []
            self.fileName = ''

        self.errorList = [] # a list of videos and error causes
        self.vidInfoList = [] # holds the data of all videos (ok or not) with url and codecs
        self.logger = self.MyLogger()
        self.vidOK = [] # list of videos that was downloaded successfully 
        self.videoFolder = './videos' #folder to save videos # default value of video destination folder

        # create movie directory if does not exist
        import os
        if not os.path.exists(self.videoFolder):
            os.makedirs(self.videoFolder)
    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    # SET THE URL FILE WITH VIDEO URL TO DOWNLOAD
    #--------------------------------------------------------------------
    def setURLList (self, videoList):
        ''' Public method to set and load file with the videos url.''' 
        self.files = self.__load_list (videoList)
        self.fileName = videoList
    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    # LOAD THE FILE WITH URL TO DOWNLOAD
    #--------------------------------------------------------------------
    def __load_list(self, fileName):
        ''' Load the .txt file with video URL to download '''

        import numpy as np
        import os.path
        if os.path.isfile(fileName):
            return np.genfromtxt(fileName,dtype='str')
        else:
            print (sysColor.Red + 'File ' + fileName + ' does not exists.' + sysColor.White)
    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    # ELIMINATE FROM STRING THE INVISIBLE CHARACTERS
    #--------------------------------------------------------------------
    def __filter_nonprintable(self, text):
        import string
        # Get the difference of all ASCII characters from the set of printable characters
        nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
        # Use translate to remove all non-printable characters
        return text.translate({ord(character):None for character in nonprintable})
    #--------------------------------------------------------------------

    #---------------------------------------------------------------------
    # CHECK IF A VIDEO URL REALLY EXISTS
    # https://docs.python.org/3.1/howto/urllib2.html
    #---------------------------------------------------------------------
    def __isOnlineVideoValid(self, url):
        '''Checks if a video exists in the internet'''

        msg = ''
        isValid = False
        req = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req)
            response.read() #page = 
            isValid = True
        except urllib.error.URLError as e:  
            if hasattr(e, 'reason'):
                msg = 'Failed to reach server:', e.reason
            elif hasattr(e, 'code'):  
                code = self.__getErrorCode(e)
                msg = 'Error code: ' + str(e) + ' ' + code

            self.errorList.append(url + ',' + self.__filter_nonprintable(str(msg) ) )
            print (sysColor.Red + "INVALID VIDEO: " + str(e) + sysColor.White + ' ' + str(url) + '\n')

        return isValid
    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    # GET THE ERROR CODE INTERACTIONG WITH THE responses DICTIONARY
    # how to iteract with dictionaries: 
    # https://stackoverflow.com/questions/7409078/iterating-over-dictionary-key-values-corresponding-to-list-in-python
    #--------------------------------------------------------------------
    def __getErrorCode(self, e):
        ''' Get the url connection error description from the error code '''
        from responseCodes import responses
        try:
            return responses[e][1]
        except:
            return 'Unknown Error'
    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    # PUBLIC METHOD TO GENERATE THE DOWNLOAD REPORTS
    #--------------------------------------------------------------------
    def saveCSVReports (self):
        if len(self.errorList) > 0:
            self.__saveReport(self.errorList, 'error_Rprt')

        if len(self.vidInfoList) > 1: #because of the header
            llist = []
            for any in self.vidInfoList:
                llist.append('Video Name,Video Codec,Audio Codec,URL')
                llist.append(any.getCodedInfo())

            self.__saveReport(llist, 'vidInfo_Rprt')
    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    # GENERIC CSV WRITER TO SAVE LISTS OF MESSAGES
    #--------------------------------------------------------------------
    def __saveReport (self, llist, fileName):
        ''' Saves a list of text objects in a csv file.
            The file output has the date-time of the creation. '''

        import datetime
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H:%M:%S") # https://www.programiz.com/python-programming/datetime/strftime

        import os
        dir = './reports/'
        if not os.path.exists(dir):
            os.makedirs(dir)

        text_file = open(dir + fileName + '_' + date_time + '_.csv', "w+")
        for any in llist:
            text_file.write( any + '\n')
        text_file.close()
    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    def getVideoList(self):
        ''' Return the list of videos with generated names to be used for the next step (inception)'''
        return self.vidOK # Return by value, no reference
    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    # TEST VIDEO DOWNLOAD 
    #--------------------------------------------------------------------   
    def __isVideoDownloadedOK (self, vidName, url):
        ''' Check if the file downloaded is a valid video '''
        import os
        from pathlib import Path
        print (sysColor.Blue + 'TEST VIDEO: ' + sysColor.White + url)
        video= Path(self.videoFolder + '/' + vidName+ '.mp4') # video was downloaded successfully
        if video.is_file():
            print (sysColor.Green + 'VALID VIDEO: ' + sysColor.White + url + '\n')
            self.vidOK.append(vidName)
        else: # check possible errors
            import glob
            if glob.glob(self.videoFolder + '/' + vidName+ '.*'): # check if the file was saved with an invalid extension
                print (sysColor.Red + "INVALID VIDEO: Missing codecs to convert to .mp4 " + sysColor.White + str(url) + '\n')
                for any in glob.glob(self.videoFolder + '/' + vidName + '.*'):
                    os.remove(any) 
                self.errorList.append (url + ',' + 'ERROR: Missing codecs to convert to .mp4')
            else:
                print (sysColor.Red + "INVALID VIDEO: Names do not match. " + sysColor.White + str(url) + '\n')
    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    # DOWNLOAD SINGLE VIDEOS
    #--------------------------------------------------------------------
    def __downloadVideo (self, url):
        ''' Downsload a single video from the URL received as parameter. ''' 

        print (sysColor.Yellow + 'DOWNLOAD ATTEMPT: ' + sysColor.White + url)
        uniqueName = self.__generateUniqueName()

        if (self.__isOnlineVideoValid(url)): # 0. Tests if URL is valid
            
            with youtube_dl.YoutubeDL(self.__getDLConfiguration(uniqueName)) as ydl:
                try:

                    # 1. get video info: https://stackoverflow.com/questions/23727943/how-to-get-information-from-youtube-dl-in-python
                    info = ydl.extract_info(url, download=False) # Retrieves a dictionary of video information
                    vid = self.VideoInfo(info, url, uniqueName)
                    self.vidInfoList.append(vid)

                    # 2. Download video
                    ydl.download([url]) 

                    # 3. test if video was downloaded correctly
                    self.__isVideoDownloadedOK(vid.getVideoName(), url)

                except youtube_dl.DownloadError as e:
                    msg = self.__filter_nonprintable(str(e))
                    self.errorList.append (url + ',ERROR: ' +  msg)
                    print (sysColor.Red + "INVALID VIDEO: " + str(e) + sysColor.White + str(url) + '\n')
    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    # DOWNLOAD VIDEOS - MAIN FUNCTION 
    #--------------------------------------------------------------------
    def download (self, url = None):
        ''' Download video, receive as parameter a video url.\n
            If passed without parameter it will download the video list '''
        if (url != None):
            self.__downloadVideo(url)
        else: # download list of videos
            if len(self.files) > 0:
                # for each url in url list 
                for url in self.files:
                    self.__downloadVideo(url)
            else:
                print (sysColor.Red + 'Video list ' + self.fileName + ' has no videos.' + sysColor.White)

    #--------------------------------------------------------------------

    #--------------------------------------------------------------------
    # RETURNS A DICTIONARY WITH THE VALID VIDEO URL, TITLE AND UNIQUE NAME
    #--------------------------------------------------------------------
    def getVideoDataDict (self):
        ''' Returns a dictionary with video name, title and url '''
        dicList = []
        for any in self.vidOK:
            for vid in self.vidInfoList:
                if (any == str(vid.vid_uname ) ):
                    ldict = dict (name=vid.vid_uname, url=vid.vid_url, title=vid.vid_title) # create a local dict to hold the data
                    dicList.append(ldict)

        return dicList
    #---------------------------------------------------------------------
        

#=========================================================================================
# END OF CLASS VIDEODOWNLOADER
#=========================================================================================
