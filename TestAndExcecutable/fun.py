import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature

lats = np.linspace(60, 90, 30)
lons = np.linspace(0, 360, 200)
X, Y = np.meshgrid(lons, lats)
Z = np.random.normal(size=X.shape)


def main():
    fig = plt.figure(figsize=[10, 5])
    ax = plt.subplot(1, 1, 1, projection=ccrs.NorthPolarStereo())
    fig.subplots_adjust(bottom=0.05, top=0.95,
                        left=0.04, right=0.95, wspace=0.02)

    # Limit the map to -60 degrees latitude and below.
    ax.set_extent([-180, 180, 60, 60], ccrs.PlateCarree())

    ax.gridlines()

    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.LAND)

    # Compute a circle in axes coordinates, which we can use as a boundary
    # for the map. We can pan/zoom as much as we like - the boundary will be
    # permanently circular.
    theta = np.linspace(0, 2 * np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)

    ax.set_boundary(circle, transform=ax.transAxes)
    ax.pcolormesh(X, Y, Z, transform=ccrs.PlateCarree())

    plt.show()


if __name__ == '__main__':
    main()
