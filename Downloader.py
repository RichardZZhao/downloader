#!/usr/bin/python2

import urllib2

from DownloaderException import DownloaderException

class Downloader():
    # Buffer size
    __blockSize = 8192

    __progressBarSize = 25

    def __sizeofFmt(self, nbytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if nbytes == 0: return '0 B'
        i = 0
        while nbytes >= 1024 and i < len(suffixes)-1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])

    def __printProgress(self, fileSize, fileSizeDownloaded):
        # Calculate the progress bar size
        barPlain = (fileSizeDownloaded * self.__progressBarSize) / fileSize
        # Create the progress bar
        status = " ["
        for index in range(1, barPlain):
            status += "="
        if barPlain == self.__progressBarSize:
            status += "="
        else:
            status += ">"
        for index in range(0, self.__progressBarSize - barPlain):
            status += " "
        status += "]"
        # Display the progress bar
        status += " %s [%3.2f%%]" % (self.__sizeofFmt(fileSizeDownloaded), fileSizeDownloaded * 100. / fileSize)
        status = status + chr(8)*(len(status)+1)
        print status,

    def download(self, url, fileName):
        if url is None:
            raise DownloaderException("Downlodaer: Source url is missing.")
        if fileName is None:
            raise DownloaderException("Downloader: Target filename is missing.")

        try:
            fd = open(fileName, 'wb')
            sock = urllib2.urlopen(url)
            meta = sock.info()
            fileSize = int(meta.getheaders("Content-Length")[0])
            print("Downloading:\nTo: %s\tSize: %s" % (fileName, self.__sizeofFmt(fileSize)))

            fileSizeDownloaded = 0
            while True:
                buffer = sock.read(self.__blockSize)
                if not buffer:
                    break

                fileSizeDownloaded += len(buffer)
                fd.write(buffer)
                self.__printProgress(fileSize, fileSizeDownloaded)
            fd.close()
        except urllib2.URLError, e:
            raise DownloaderException("Downloader: " + str(e))
        except ValueError:
            raise DownloaderException("Downloader: " + str(ValueError))
