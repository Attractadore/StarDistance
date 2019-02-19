import numpy
import PIL
from PIL import Image
import sys
from math import sqrt
from matplotlib import pyplot


def distance(image, perc):
    im_data = to_gs_arr(image, perc)
    im_data = numpy.squeeze(numpy.split(im_data, 2, axis=1)[0])
    # im_center = to_gs_arr(image, 0.01)
    # im_center = numpy.squeeze(numpy.split(im_center, 2, axis=1)[0])
    # im_center = to_gs_arr(image, 0.1)
    # im_center = numpy.squeeze(numpy.split(im_center, 2, axis=1)[0])
    # while len(im_center) > 0:
    #     im_data.remove(im_center.pop())
    # print("Image size {0} center size {1}".format(im_data.size, im_center.size))
    # im_data = list(im_data)
    # im_center = list(im_center)
    # while len(im_center) > 0:
    #     print(len(im_center))
    #     im_data.remove(im_center.pop())
    # im_data = numpy.asarray(im_data)
    # print("Resized image size {0}".format(im_data.size))

    # m = numpy.median(im_data)/255
    m = numpy.average(im_data)/255
    # m_c = numpy.average(im_center)/255
    # d = [abs(m - x/255) for x in im_data]
    d = [abs(m - x/255) for x in im_data]
    # d_c = [abs(m_c - x/255) for x in im_center]
    fluc = numpy.average(d)
    # fluc_c = numpy.average(d_c)
    return fluc
    # return (fluc * im_data.size - fluc_c * im_center.size) / (im_data.size - im_center.size)


def to_gs_arr(img, perc=0.5):
    im = Image.open(img).convert("LA")
    w, h = im.size
    ratio = sqrt(perc)
    im = im.crop((w * (1 - ratio) / 2, h * (1 - ratio) / 2, w * (1 + ratio) / 2, h * (1 + ratio) / 2))
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
                print("Ignoring {0}".format(inp[1]))
                continue
            d = float(inp[1])
            s = float(inp[2])
            # s = 0.2
            fluc = distance(i, s)
            # if i[:5] == "data/":
            #     fluc *= 0.7
            # fluc += 20/(d ** 2)
            flucs.append(fluc)
            distances.append(d)
            print("{2} Distance {0} fluctuation {1}".format(d, fluc, i))
            # pyplot.scatter(d, fluc)
        m_fluc = numpy.median(flucs)
        # corrected_flucs = [(m_fluc + (x - m_fluc) * k) for x in flucs]
        pyplot.ylim(0, 0.3)
        pyplot.scatter(distances, flucs)

        pyplot.show()


if __name__ == "__main__":
    main()
