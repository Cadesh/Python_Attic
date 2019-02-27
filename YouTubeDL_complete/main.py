
#from videoDL import VideoDownloader
#from sysColor import sysColor

def main ():

    videoFolder = './videos' #folder to save videos

    # import sys
    # # ADD COMMNONS PATH
    # sys.path.insert(0, './0. Commons')
    from sysColor import sysColor

    # # ADD DOWNLOADER PATH
    # sys.path.insert(0, './1. Downloader')
    from videoDL import VideoDownloader

    # ADD INCEPTION PATH
    # sys.path.insert(0, './2. Inception')
    # from inception import InceptionEvaluator 
    # from tfProcess import tfProcess
    # from inceptionSingle import InceptionSingle

    sysColor.clearTerminal()
    sysColor.printTitle('1. VIDEO DOWNLOADER')

    # THERE ARE THREE WAYs TO USE DOWNLOADER TO DOWNLOAD VIDEOS

    # 1. USE A LIST OF URL LOADEAD FROM A FILE. THE FILE NAME IS PASSED AS ARGUMENT 1
    #vd1 = VideoDownloader(sys.argv[1]) # The parameter is a name of file with vidoes url
    #vd1.download()

    # 2. YOU CAN ALSO DEFINE A CLASS AND CALL METHOD DOWNLOAD WITH THE URL AS PARAMETER. 
    #vd2 = VideoDownloader() 
    #vd2.download('https://www.facebook.com/thevintagenews/videos/1993930357348735/UzpfSTcxMjI5MjAxODg0NTkxNTpWSzoxOTkzOTMwMzU3MzQ4NzM1/')

    # 3. THE FINAL OPTION IS TO DEFINE A DOWNLOADER AND LATER SET A FILE WITH THE URL LIST.
    vd3 = VideoDownloader() 
    vd3.setVideoFolder(videoFolder) # define the folder to save the downloaded videos
    vd3.setURLList ('list.txt')     # define the txt file witht the list of url
    vd3.download()                  # start the download of videos
    vd3.saveCSVReports()            # save the csv reports on video downloads

main()
