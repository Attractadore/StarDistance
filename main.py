import numpy
import PIL
from PIL import Image
import sys
from math import sqrt
from matplotlib import pyplot

def distance(image,perc):
    im_data = to_gs_arr(image,perc)
    # print(im_data.shape)
    s = (im_data.shape[0], 1)
    im_data = numpy.squeeze(numpy.split(im_data, 2, axis=1)[0])
    m = numpy.median(im_data)/255
    d = [abs(m - x/255) for x  in im_data]
    fluc = numpy.average(d)
    # print(numpy.average(d))

    # return 0
    return  fluc

def to_gs_arr(img, perc=0.5):
    im = Image.open(img).convert("LA")
    w, h = im.size
    ratio = sqrt(perc)
    im = im.crop((w * (1 - ratio) / 2 , h * (1 - ratio) / 2, w * (1 + ratio) / 2, h * (1 + ratio) / 2))
    return numpy.asarray(im.getdata())



def main1():
    distance(sys.argv[1], float(sys.argv[2]))

    return 0

def main():
    rf = sys.argv[1]
    with open(rf, "r") as f:
        x = []
        y = []
        for line in f:
            i, d, s = line.replace("\n", "").split(" ")
            d = float(d)
            s = float(s)
            fluc = distance(i, s)
            print("Distance {0} fluctuation {1}".format(d, fluc))
            pyplot.scatter(d, fluc)
            # x.append(d)
            # y.append(fluc)

        # x = numpy.asarray(x)
        # y = numpy.asarray(y)
        # pyplot.scatter(x, y)
        pyplot.show()


if __name__ == "__main__":
    main()