import numpy
import PIL
from PIL import Image
import sys
from math import sqrt
from matplotlib import pyplot


def distance(image, perc):
    im_data = to_gs_arr(image,perc)
    s = (im_data.shape[0], 1)
    im_data = numpy.squeeze(numpy.split(im_data, 2, axis=1)[0])
    m = numpy.median(im_data)/255
    d = [abs(m - x/255) for x  in im_data]
    fluc = numpy.average(d)
    return fluc


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
    k = float(sys.argv[2])
    with open(rf, "r") as f:
        distances = []
        flucs = []
        for line in f:
            inp = line.replace("\n", "").split(" ")
            i = inp[0]
            # d = inp[1]
            # s = inp[2]
            # i, d, s = line.replace("\n", "").split(" ")
            if i == "#":
                continue
            d = float(inp[1])
            s = float(inp[2])
            fluc = distance(i, s)
            flucs.append(fluc)
            distances.append(d)
            print("Distance {0} fluctuation {1}".format(d, fluc))
            # pyplot.scatter(d, fluc)
        m_fluc = numpy.median(flucs)
        corrected_flucs = [(m_fluc + (x - m_fluc) * k) for x in flucs]
        pyplot.ylim(0, 0.3)
        pyplot.scatter(distances, corrected_flucs)

        pyplot.show()


if __name__ == "__main__":
    main()
