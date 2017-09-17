from PIL import Image, ImageDraw

""" Need to Implement output --> url;color;color;color """
import csv
import requests
import cStringIO
import urllib2
from multiprocessing import Pool, TimeoutError

def get_colors(infile, outfile, numcolors=4, swatchsize=20, resize=150):

    image = Image.open(infile)
    image = image.resize((resize, resize))
    result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
    result.putalpha(0)
    colors = result.getcolors(resize*resize)
    print colors[1:]

    # Save colors to file

    pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
    draw = ImageDraw.Draw(pal)

    posx = 0
    for count, col in colors:
        draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
        posx = posx + swatchsize

    del draw
    pal.save(outfile, "PNG")

if __name__ == '__main__':
    get_colors('images/Image1.jpg', 'images/out1.png')