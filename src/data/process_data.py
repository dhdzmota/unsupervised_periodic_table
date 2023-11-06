import numpy as np
import os
import pandas as pd

from src.data.process_utils import (
    oxidation_states_nb,
    neg_oxidation_states_nb,
    oxidation_state_operation,
    step_between_oxidation_states,
    electron_conf_after_noble_gas_list_operation,
    electron_conf_last_letter,
    electron_conf_highest_letter,
    electron_conf_last_level,
    electron_conf_last_value,
    state_text_parse,
)
from src.data.download_data import save_as_csv, read_data_as_csv


def process_periodic_table_df(periodic_table):
    periodic_table_cleaned = pd.DataFrame()

    periodic_table_cleaned['atomic_mass'] = periodic_table.AtomicMass
    periodic_table_cleaned['atomic_mass_over_atomic_nb'] = (
            periodic_table.AtomicMass / periodic_table.index
    )
    periodic_table_cleaned['atomic_radius_over_atomic_nb'] = (
            periodic_table.AtomicRadius / periodic_table.index
    )
    periodic_table_cleaned['atomic_radius_over_ionization_energy'] = (
            periodic_table.AtomicRadius / periodic_table.IonizationEnergy
    )
    periodic_table_cleaned['electronegativity'] = (
        periodic_table.Electronegativity
    )
    periodic_table_cleaned['atomic_radius'] = periodic_table.AtomicRadius
    periodic_table_cleaned['ionization_energy'] = (
        periodic_table.IonizationEnergy
    )
    periodic_table_cleaned['electron_affinity'] = (
        periodic_table.ElectronAffinity
    )
    periodic_table_cleaned['oxidation_states_nb'] = (
        periodic_table.OxidationStates.apply(oxidation_states_nb)
    )
    periodic_table_cleaned['neg_oxidation_states_nb'] = (
        periodic_table.OxidationStates.apply(neg_oxidation_states_nb)
    )
    periodic_table_cleaned['oxidation_state_max'] = (
        periodic_table.OxidationStates.apply(
            oxidation_state_operation,
            operation=np.nanmax)
    )
    periodic_table_cleaned['oxidation_state_min'] = (
        periodic_table.OxidationStates.apply(
            oxidation_state_operation,
            operation=np.nanmin
        )
    )
    periodic_table_cleaned['oxidation_state_steps'] = (
        periodic_table.OxidationStates.apply(
            oxidation_state_operation,
            operation=step_between_oxidation_states
        )
    )
    periodic_table_cleaned['oxidation_state_range'] = (
            periodic_table_cleaned['oxidation_state_max']
            - periodic_table_cleaned['oxidation_state_min']
    )
    periodic_table_cleaned['standard_state'] = (
        periodic_table.StandardState.apply(state_text_parse)
    )
    periodic_table_cleaned['melting_point'] = periodic_table.MeltingPoint
    periodic_table_cleaned['boiling_point'] = periodic_table.BoilingPoint

    periodic_table_cleaned[
        'melting_boiling_point_difference'] = (
            periodic_table.MeltingPoint - periodic_table.BoilingPoint
    )

    # periodic_table_cleaned['atomic_mass_over_density'] = (
    # periodic_table.AtomicMass / periodic_table.Density
    # )

    periodic_table_cleaned['electron_conf_after_noble_gas_nb'] = (
        periodic_table.ElectronConfiguration.apply(
            electron_conf_after_noble_gas_list_operation,
            operation=len
        )
    )
    periodic_table_cleaned['electron_conf_last_orbital'] = (
        periodic_table.ElectronConfiguration.apply(
            electron_conf_after_noble_gas_list_operation,
            operation=electron_conf_last_letter)
    )
    periodic_table_cleaned['electron_conf_last_energy_level'] = (
        periodic_table.ElectronConfiguration.apply(
            electron_conf_after_noble_gas_list_operation,
            operation=electron_conf_last_level
        )
    )
    periodic_table_cleaned['electron_conf_electron_hold'] = (
        periodic_table.ElectronConfiguration.apply(
            electron_conf_after_noble_gas_list_operation,
            operation=electron_conf_last_value
        )
    )
    periodic_table_cleaned['electron_conf_highest_orbital'] = (
        periodic_table.ElectronConfiguration.apply(
            electron_conf_after_noble_gas_list_operation,
            operation=electron_conf_highest_letter
        )
    )

    periodic_table_cleaned['group_block'] = periodic_table.GroupBlock

    # HardCoded Noble gas electronegativity and Electron Affinity:
    noble_gas = 2, 10, 18
    for element in noble_gas:
        periodic_table_cleaned.loc[element, 'electronegativity'] = 0
        periodic_table_cleaned.loc[element, 'electron_affinity'] = 0

    periodic_table_cleaned.loc[36, 'electron_affinity'] = 0
    periodic_table_cleaned.loc[54, 'electron_affinity'] = 0
    periodic_table_cleaned.loc[86, 'electron_affinity'] = 0
    return periodic_table_cleaned


if __name__ == '__main__':
    file_path = os.path.dirname(os.path.abspath(__file__))
    general_path = os.path.join(file_path, '..', '../')
    data_raw_path = os.path.join(general_path, 'data', 'raw')
    data_interim_path = os.path.join(general_path, 'data', 'interim')
    data_raw_filename = os.path.join(data_raw_path, 'periodic_table_data.csv')
    data_interim_filename = os.path.join(
        data_interim_path,
        'periodic_table_data_processed.csv'
    )
    periodic_table_df = read_data_as_csv(data_raw_filename, keep_na=True)
    cleaned_data = process_periodic_table_df(periodic_table_df)
    save_as_csv(data_interim_filename, cleaned_data)
