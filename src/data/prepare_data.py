import os
import pandas as pd
import numpy as np

from src.data.download_data import save_as_csv, read_data_as_csv
from src.data.process_utils import (
    PHASE_DICT,
    ELECTRON_CONFIGURATION,
    NON_USABLE_FEATURES,
    LOG_FEATURES
)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler  # , StandardScaler, Normalizer
from sklearn.impute import KNNImputer  # , SimpleImputer,


def apply_pipeline(transformed_pt, df_index):
    minmax_scaler = MinMaxScaler(feature_range=(0, 1))
    knn_inputer = KNNImputer(
        missing_values=np.nan,
        n_neighbors=4,
        weights='distance',
    )
    pipe = Pipeline([
        ('scaler1', minmax_scaler),
        # ('scaler2', StandardScaler()),
        ('inputer1', knn_inputer),
        # ('inputer2', SimpleImputer(
        # missing_values=np.nan, strategy='mean', fill_value=10)),
        # ('scaler3', Normalizer())
    ])

    pipe.fit(transformed_pt)
    transformed_pt = pd.DataFrame(
        pipe.transform(transformed_pt),
        columns=transformed_pt.columns,
        index=df_index
    )
    return transformed_pt


def apply_transformations(transformed_pt):
    transformed_pt['standard_state'] = transformed_pt.standard_state.apply(
        lambda x: PHASE_DICT.get(x))
    transformed_pt['electron_conf_last_orbital'] = (
        transformed_pt.electron_conf_last_orbital.apply(
            lambda x: ELECTRON_CONFIGURATION.get(x)
        )
    )
    transformed_pt['electron_conf_highest_orbital'] = (
        transformed_pt.electron_conf_highest_orbital.apply(
            lambda x: ELECTRON_CONFIGURATION.get(x)
        )
    )
    transformed_pt.drop(NON_USABLE_FEATURES, axis=1, inplace=True)

    nan_vals = transformed_pt.isna().sum(axis=1) / transformed_pt.shape[1]
    transformed_pt = transformed_pt[nan_vals < nan_vals.quantile(0.90)]
    temporal_tpt_index = transformed_pt.index
    if LOG_FEATURES:
        for feature in LOG_FEATURES:
            transformed_pt[f'{feature}'] = np.log(transformed_pt[feature] + 1)

    transformed_pt = apply_pipeline(transformed_pt, temporal_tpt_index)
    return transformed_pt


if __name__ == '__main__':
    file_path = os.path.dirname(os.path.abspath(__file__))
    general_path = os.path.join(file_path, '..', '../')
    data_interim_path = os.path.join(general_path, 'data', 'interim')
    data_processed_path = os.path.join(general_path, 'data', 'processed')
    data_interim_filename = os.path.join(
        data_interim_path,
        'periodic_table_data_processed.csv'
    )
    data_processed_filename = os.path.join(
        data_processed_path,
        'processed_data.csv'
    )
    periodic_table = read_data_as_csv(data_interim_filename, keep_na=True)
    periodic_table_transformed = apply_transformations(periodic_table)
    save_as_csv(data_processed_filename, periodic_table_transformed)
