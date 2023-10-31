import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


SPLIT_VAL = '<tr><td  align=right>'
HTML_TAG1 = 'a'
HTML_TAG2 = 'td'
MIN_ATOMIC_NB = 1
MAX_ATOMIC_NB = 118
ZFILL_VAL = 3
URL_LINK = 'https://periodictable.com/Elements/{}/data.html'


def get_element_data_from_url(url):
    element_information = {}
    url_info = requests.get(url)
    # To know which elements, an inspection to the desired url must be done.
    url_info_tag = url_info.text.split(SPLIT_VAL)
    for tag_inf in url_info_tag:
        soup = BeautifulSoup(tag_inf, features="html.parser")
        element_property = soup.find(HTML_TAG1).text
        element_value = soup.find(HTML_TAG2).text
        element_information[element_property] = element_value
    return element_information


def fill_periodic_table_dictionary():
    periodic_table = {}
    for element in range(MIN_ATOMIC_NB, MAX_ATOMIC_NB+1):
        element_nb = str(element).zfill(ZFILL_VAL)
        link = URL_LINK.format(element_nb)
        periodic_table[f'{element_nb}'] = get_element_data_from_url(link)
    return periodic_table


def transform_periodic_table_dict_to_df(periodic_table_dict):
    periodic_table_df_t = pd.DataFrame(periodic_table_dict)
    # Non usable column
    periodic_table_df_t.drop('H', inplace=True)
    periodic_table_df = periodic_table_df_t.T
    return periodic_table_df


def save_as_csv(path, df):
    df.to_csv(path)


if __name__ == '__main__':
    file_path = os.path.dirname(os.path.abspath(__file__))
    general_path = os.path.join(file_path, '..', '../')
    data_raw_path = os.path.join(general_path, 'data', 'raw')
    data_raw_filename = os.path.join(data_raw_path, 'data.csv')

    periodic_table_dict = fill_periodic_table_dictionary()
    data = transform_periodic_table_dict_to_df(
        periodic_table_dict=periodic_table_dict
    )
    save_as_csv(data_raw_filename, data)
