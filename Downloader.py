from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

max_attempt = 10


class Downloader:
    def __init__(self, str_username, str_password, str_link):
        self.api = SentinelAPI(str_username, str_password, str_link)
        self.products = None

    def search_polygon(self, footprint, str_date_start, str_date_end, str_platform_name, percentage):
        print('searching')
        self.products = self.api.query(footprint,
                                       date=(str_date_start, str_date_end),
                                       platformname=str_platform_name,
                                       cloudcoverpercentage=(percentage[0], percentage[1]))
        size = self.api.get_products_size(self.products)
        print(f'found {size} of data')

    def download_products(self, path):
        self.api.download_all(self.products, directory_path=path, max_attempts=max_attempt, checksum=True)
        print('downloaded')
        df_products = self.api.to_dataframe(self.products)
        return df_products



