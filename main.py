from PIL import Image
import cStringIO
import urllib2
from multiprocessing import Pool, TimeoutError
import multiprocessing
import time
import csv


""" Need to Implement output --> url;color;color;color """

# SET URLS
URLs = []
with open('data/urls.txt', 'r') as f:
    # read data as lines of text
    URLs = [x.splitlines()[0] for x in list(f.readlines())]
    URLs = list(set(URLs))


# COLOR GRABBER - https://gist.github.com/zollinger/1722663 
def getColors(infile, numcolors=3, resize=150):

    image = Image.open(infile)                                              # Using PIL open image
    image = image.resize((resize, resize))                                  # resize image to reduce pixel set
    result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)   # Convert to image pallete to get dominant colors
    result.putalpha(0)                                                      # Set alpha to zero for RGB
    colors = result.getcolors(resize*resize)                                # get colors in RGB of the resized image
    colors = [y[:-1] for y in [x[-1] for x in colors]]                      # take RGB values
    return colors

# URL READER
def readImage(url):
    fl = None
    try:
        fl = cStringIO.StringIO(urllib2.urlopen(url).read())                # create image data from URL string
    except:
        print "Could not Download Image from Url"

    return (url, getColors(fl))                                             # Return the formatted data string

if __name__ == '__main__':
    import timeit
    time = timeit.default_timer()
    numCPUs = multiprocessing.cpu_count()
    try:
        pool = Pool(processes=numCPUs*4)                                    # Pool processes using 4 times the CPUs for optimal performance time
        data = pool.map(readImage, URLs)                                    
    except TimeoutError:
        print "Error, image downloading Timed Out"

    with open("data/output.csv", 'wb') as csvFile:                          # Create CSV file
        lineWriter = csv.writer(csvFile)
        for line in data:
            lineWriter.writerow((line[0], line[1][0], line[1][1], line[1][2]))

    print("wall Time: ", timeit.default_timer() - time) 









