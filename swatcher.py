from PIL import Image, ImageDraw
import cStringIO
import urllib2
from multiprocessing import Pool, TimeoutError
import multiprocessing
import time
import csv

import timeit

time = timeit.default_timer()

def get_colors(infile, outfile, numcolors=3, swatchsize=20, resize=150):

    image = Image.open(infile)
    image = image.resize((resize, resize))
    result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
    result.putalpha(0)
    colors = result.getcolors(resize*resize)

    # Save colors to file

    pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
    draw = ImageDraw.Draw(pal)

    posx = 0
    for count, col in colors:
        draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
        posx = posx + swatchsize

    del draw
    pal.save(outfile, "PNG")
    print infile, "saved as", outfile

def readImage(url):
    fl = None
    try:
        fl = cStringIO.StringIO(urllib2.urlopen(url).read())                # create image data from URL string
    except:
        print "Could not Download Image from Url"

    
    return fl


URLs = []
with open('data/urls.txt', 'r') as f:
    # read data as lines of text
    URLs = [x.splitlines()[0] for x in list(f.readlines())] 

for i, url in enumerate(URLs):
    infile = readImage(url)
    get_colors(infile, 'images/outfile' + str(i) + '.png')

print("wall Time: ", timeit.default_timer() - time) 