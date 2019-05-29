from sentinelsat import SentinelAPI

max_attempt = 10


class Downloader:
    def __init__(self, str_username, str_password, str_link):
        self.api = SentinelAPI(str_username, str_password, str_link)
        self.products = None

    def search_polygon(self, footprint: object, str_date_start: str,
                       str_date_end: str, str_platform_name: str, percentage: object):
        print('searching')
        self.products = self.api.query(footprint,
                                       date=(str_date_start, str_date_end),
                                       platformname=str_platform_name,
                                       cloudcoverpercentage=(percentage[0], percentage[1]))
        size = self.api.get_products_size(self.products)
        print(f'found {size}GiB of data')
        # print(self.products)

    def download_zip(self, path):
        self.api.download_all(self.products, path, max_attempt, True)

    def download_products(self, path, download_file):
        if download_file:
            self.download_zip(path)
        print('downloaded')
        df_products = self.api.to_dataframe(self.products)
        return df_products

    def download_geoproduct(self, path, download_file):
        if download_file:
            self.download_zip(path)
        # print('download Geos')
        gdf_products = self.api.to_geodataframe(self.products)
        return gdf_products

    def download_json(self):
        return self.api.to_geojson(self.products)

    def download_one(self, key, path):
        self.api.download(key, path, True)


