
#-------------------------------------------------------------------
# USED TO SHOW COLOR IN TERMINAL
#-------------------------------------------------------------------
class sysColor:
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'

    #-------------------------------------------------------------------
    # CLEAR THE TERMINAL SCREEN
    # platform.system() identifies the OS 'Linux', 'Windows' or 'Darwin'(for MacOS)
    #-------------------------------------------------------------------
    def clearTerminal():
        import platform
        import os
        if ( platform.system() == 'Windows'): os.system('cls')
        else: os.system('clear')
    #-------------------------------------------------------------------

    def printTitle (title):

        space = int((40 - len(title))/2) # used to set the title in the middle
        spaces = ''
        for i in range (1,space):
            spaces += ' ' # add space 
        print (sysColor.Cyan + '---------------------------------------')  
        print (spaces +  sysColor.Yellow + title)
        print (sysColor.Cyan + '---------------------------------------\n' + sysColor.White)
