import numpy
from PIL import Image
import sys
from math import sqrt
from matplotlib import pyplot
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def measure_fluctuation_squares(img, perc, square_side=10):
    im = load_gs_image(img, perc)
    w, h = im.size
    crop_w = int(w/square_side)
    crop_h = int(h/square_side)
    ims = [None] * (square_side ** 2)
    for i in range(square_side ** 2):
        cs_w = crop_w * (i % square_side)
        cs_h = crop_h * (i // square_side)
        cropped_im = im.crop((cs_w, cs_h, cs_w + crop_w, cs_h + crop_h))
        ims[i] = cropped_im
    im = None
    flucs = [measure_fluctuation(im, perc) for im in ims]
    return numpy.average(flucs)


def measure_fluctuation(img, perc):
    if type(img) == str:
        img = load_gs_image(img, perc)
    im_data = numpy.asarray(img.getdata())
    im_data = numpy.squeeze(numpy.split(im_data, 2, axis=1)[0])
    m = numpy.average(im_data)/255
    d = [abs(m - x/255) for x in im_data]
    fluc = numpy.average(d)
    return fluc


def load_gs_image(img, perc=0.5):
    im = Image.open(img).convert("LA")
    w, h = im.size
    ratio = sqrt(perc)
    im = im.crop((w * (1 - ratio) / 2, h * (1 - ratio) / 2, w * (1 + ratio) / 2, h * (1 + ratio) / 2))
    return im


def main():
    rf = sys.argv[1]
    # k = float(sys.argv[2])
    with open(rf, "r") as f:
        distances = []
        # fluc_funcs = [measure_fluctuation, measure_fluctuation_squares]
        # fluc_funcs = [measure_fluctuation_squares]
        fluc_funcs = [measure_fluctuation]
        flucs = [list() for _ in range(len(fluc_funcs))]
        for line in f:
            inp = line.replace("\n", "").split(" ")
            im = inp[0]
            if im == "#":
                print("{0} ignored".format(inp[1]))
                continue
            d = float(inp[1])
            p = float(inp[2])

            try:
                for i in range(len(fluc_funcs)):
                    fluc_func = fluc_funcs[i]
                    res = fluc_func(im, p)
                    flucs[i].append(res)
            except FileNotFoundError:
                print("{0} not found".format(im))
                continue

            distances.append(float(inp[1]))
            print("{0} at {1}k ly away".format(im, d))

        pyplot.xlim(2, max(distances) + 10)
        pyplot.ylim(0, 0.3)
        # pyplot.ylim(0.01, 1)
        # pyplot.xscale("log")
        # pyplot.yscale("log")
        # inverse_distances = [1 / d for d in distances]
        poly = PolynomialFeatures(degree=2)
        # inverse_distances = numpy.divide(1, numpy.split(poly.fit_transform(numpy.asarray(distances).reshape(-1, 1)), 3, axis=1)[-1])
        inverse_distances = numpy.divide(1, numpy.cbrt(distances)).reshape(-1, 1)
        print(inverse_distances)
        for f in flucs:
            clf = LinearRegression()
            clf.fit(inverse_distances, f)
            test_data = numpy.linspace(0.01, max(distances) + 10, 500)
            # inverse_test_data = numpy.divide(1, numpy.split(poly.fit_transform(numpy.asarray(test_data).reshape(-1, 1)), 3, axis=1)[-1])
            inverse_test_data = numpy.divide(1, numpy.cbrt(test_data)).reshape(-1, 1)
            test_flucs = clf.predict(inverse_test_data)
            pyplot.plot(test_data, test_flucs, color="red")
            pyplot.scatter(distances, f)

        for e in zip(flucs[0], distances):
            print("{0}, {1}".format(e[0], e[1]))

        pyplot.show()


if __name__ == "__main__":
    main()
