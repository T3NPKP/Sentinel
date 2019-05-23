from osgeo import gdal

verbose = 0
quiet = 0

def raster_copy(s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,
                t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n,
                nodata=None):
    if nodata is not None:
        return raster_copy_with_nodata(
            s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,
            t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n,
            nodata)

    if verbose != 0:
        print('Copy %d,%d,%d,%d to %d,%d,%d,%d.' \
              % (s_xoff, s_yoff, s_xsize, s_ysize,
                 t_xoff, t_yoff, t_xsize, t_ysize))

    s_band = s_fh.GetRasterBand(s_band_n)
    t_band = t_fh.GetRasterBand(t_band_n)

    data = s_band.ReadRaster(s_xoff, s_yoff, s_xsize, s_ysize,
                             t_xsize, t_ysize, t_band.DataType)
    t_band.WriteRaster(t_xoff, t_yoff, t_xsize, t_ysize,
                       data, t_xsize, t_ysize, t_band.DataType)

    return 0


def raster_copy_with_nodata(s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,
                            t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n,
                            nodata):
    try:
        import numpy as Numeric
    except ImportError:
        import Numeric

    if verbose != 0:
        print('Copy %d,%d,%d,%d to %d,%d,%d,%d.' \
              % (s_xoff, s_yoff, s_xsize, s_ysize,
                 t_xoff, t_yoff, t_xsize, t_ysize))

    s_band = s_fh.GetRasterBand(s_band_n)
    t_band = t_fh.GetRasterBand(t_band_n)

    data_src = s_band.ReadAsArray(s_xoff, s_yoff, s_xsize, s_ysize,
                                  t_xsize, t_ysize)
    data_dst = t_band.ReadAsArray(t_xoff, t_yoff, t_xsize, t_ysize)

    nodata_test = Numeric.equal(data_src, nodata)
    to_write = Numeric.choose(nodata_test, (data_src, data_dst))

    t_band.WriteArray(to_write, t_xoff, t_yoff)

    return 0


class file_info:
    """A class holding information about a GDAL file."""

    def init_from_name(self, filename):
        """
        Initialize file_info from filename
        filename -- Name of file to read.
        Returns 1 on success or 0 if the file can't be opened.
        """
        fh = gdal.Open(filename)
        if fh is None:
            return 0

        self.filename = filename
        self.bands = fh.RasterCount
        self.xsize = fh.RasterXSize
        self.ysize = fh.RasterYSize
        self.band_type = fh.GetRasterBand(1).DataType
        self.projection = fh.GetProjection()
        self.geotransform = fh.GetGeoTransform()
        self.ulx = self.geotransform[0]
        self.uly = self.geotransform[3]
        self.lrx = self.ulx + self.geotransform[1] * self.xsize
        self.lry = self.uly + self.geotransform[5] * self.ysize

        ct = fh.GetRasterBand(1).GetRasterColorTable()
        if ct is not None:
            self.ct = ct.Clone()
        else:
            self.ct = None

        return 1

    def report(self):
        print('Filename: ' + self.filename)
        print('File Size: %dx%dx%d' \
              % (self.xsize, self.ysize, self.bands))
        print('Pixel Size: %f x %f' \
              % (self.geotransform[1], self.geotransform[5]))
        print('UL:(%f,%f)   LR:(%f,%f)' \
              % (self.ulx, self.uly, self.lrx, self.lry))

    def copy_into(self, t_fh, s_band=1, t_band=1, nodata_arg=None):
        """
        Copy this files image into target file.
        This method will compute the overlap area of the file_info objects
        file, and the target gdal.Dataset object, and copy the image data
        for the common window area.  It is assumed that the files are in
        a compatible projection ... no checking or warping is done.  However,
        if the destination file is a different resolution, or different
        image pixel type, the appropriate resampling and conversions will
        be done (using normal GDAL promotion/demotion rules).
        t_fh -- gdal.Dataset object for the file into which some or all
        of this file may be copied.
        Returns 1 on success (or if nothing needs to be copied), and zero one
        failure.
        """
        t_geotransform = t_fh.GetGeoTransform()
        t_ulx = t_geotransform[0]
        t_uly = t_geotransform[3]
        t_lrx = t_geotransform[0] + t_fh.RasterXSize * t_geotransform[1]
        t_lry = t_geotransform[3] + t_fh.RasterYSize * t_geotransform[5]

        # figure out intersection region
        tgw_ulx = max(t_ulx, self.ulx)
        tgw_lrx = min(t_lrx, self.lrx)
        if t_geotransform[5] < 0:
            tgw_uly = min(t_uly, self.uly)
            tgw_lry = max(t_lry, self.lry)
        else:
            tgw_uly = max(t_uly, self.uly)
            tgw_lry = min(t_lry, self.lry)

        # do they even intersect?
        if tgw_ulx >= tgw_lrx:
            return 1
        if t_geotransform[5] < 0 and tgw_uly <= tgw_lry:
            return 1
        if t_geotransform[5] > 0 and tgw_uly >= tgw_lry:
            return 1

        # compute target window in pixel coordinates.
        tw_xoff = int((tgw_ulx - t_geotransform[0]) / t_geotransform[1] + 0.1)
        tw_yoff = int((tgw_uly - t_geotransform[3]) / t_geotransform[5] + 0.1)
        tw_xsize = int((tgw_lrx - t_geotransform[0]) / t_geotransform[1] + 0.5) \
                   - tw_xoff
        tw_ysize = int((tgw_lry - t_geotransform[3]) / t_geotransform[5] + 0.5) \
                   - tw_yoff

        if tw_xsize < 1 or tw_ysize < 1:
            return 1

        # Compute source window in pixel coordinates.
        sw_xoff = int((tgw_ulx - self.geotransform[0]) / self.geotransform[1])
        sw_yoff = int((tgw_uly - self.geotransform[3]) / self.geotransform[5])
        sw_xsize = int((tgw_lrx - self.geotransform[0]) \
                       / self.geotransform[1] + 0.5) - sw_xoff
        sw_ysize = int((tgw_lry - self.geotransform[3]) \
                       / self.geotransform[5] + 0.5) - sw_yoff

        if sw_xsize < 1 or sw_ysize < 1:
            return 1

        # Open the source file, and copy the selected region.
        s_fh = gdal.Open(self.filename)

        return \
            raster_copy(s_fh, sw_xoff, sw_yoff, sw_xsize, sw_ysize, s_band,
                        t_fh, tw_xoff, tw_yoff, tw_xsize, tw_ysize, t_band,
                        nodata_arg)

