import astropy.io.fits as pyfits
from astropy.io.fits import Header
from numpy.core import array

from external.cosmics import CosmicsImage
from common.image import Image


def load(filepath):
    """

    :param filepath: fits image path
    :return: an Image
    """
    data = pyfits.getdata(filepath, hdu=0)
    primary = Header(pyfits.getheader(filepath, 0))
    headers = [primary]
    extcount = int(primary.get("NEXTEND", 0))

    for idx in range(1, extcount):
        ext = Header(pyfits.getheader(filepath, idx))
        headers.append(ext)
    return Image(array(data), headers)


def obtain_cr(raw, mask=None, iterations=4)->array:
    img = CosmicsImage(raw)
    img.clean(mask, True)
    img.run(maxiter=iterations)

    return array(img.cleanarray), img.getmask()
