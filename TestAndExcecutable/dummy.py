try:
    src_ds = gdal.Open( "INPUT.tif" )
except (RuntimeError, e):
    print ('Unable to open INPUT.tif')
    print (e)
    sys.exit(1)

try:
    srcband = src_ds.GetRasterBand(1)
except (RuntimeError):
    # for example, try GetRasterBand(10)
    print ('Band ( %i ) not found' % band_num)
    sys.exit(1)