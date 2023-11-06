import pandas as pd
import os

URL_LINK = 'https://pubchem.ncbi.nlm.nih.gov' \
            '/rest/pug/periodictable/' \
            'CSV?response_type=save&response_basename=PubChemElements_all'


def save_as_csv(path, df):
    df.to_csv(path)


def read_data_as_csv(path, keep_na=False):
    df = pd.read_csv(
        path,
        index_col=0,
        keep_default_na=keep_na
    )
    return df


def get_periodic_table(url):
    periodic_table_df = read_data_as_csv(url, keep_na=True)
    return periodic_table_df


if __name__ == '__main__':
    file_path = os.path.dirname(os.path.abspath(__file__))
    general_path = os.path.join(file_path, '..', '../')
    data_raw_path = os.path.join(general_path, 'data', 'raw')
    data_raw_filename = os.path.join(data_raw_path, 'periodic_table_data.csv')
    data = get_periodic_table(URL_LINK)
    save_as_csv(data_raw_filename, data)
