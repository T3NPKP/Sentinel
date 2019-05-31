from scipy.misc import bytescale
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def transform_north(lons, lats):
    pts = north_crs.transform_points(north_xform_crs, lons, lats)
    x = pts[..., 0]
    y = pts[..., 1]
    return x, y


north_crs = ccrs.Orthographic(65, 90)
north_globe = ccrs.Globe(semiminor_axis=90)
north_xform_crs = ccrs.Geodetic(globe=north_globe)


# fig = plt.figure()
# ax = plt.axes(projection=north_crs)
#
# lons, lats = transform_north()
# ax.pcolormesh(lons, lats, r, transform=north_crs, color=colorTuple)
#
#
# plt.savefig(args.output, format="png", bbox_inches='tight')

