import pandas as pd
import os

from src.data.clean_utils import (
    atomic_weight_clean,
    density_clean,
    temp_point_clean,
    pressure_clean,
    heat_clean,
    specific_heat_clean,
    adiabatic_index_clean,
    thermal_conductivity_clean,
    thermal_expansion_clean,
    molar_volume_clean,
    speed_clean,
    coef_clean,
    conductivity_clean,
    resistivity_clean,
    radius_clean,
    lattice_constants_clean,
    isotopic_clean,
)
from src.data.download_data import save_as_csv, read_data_as_csv


def clean_periodic_table_df(periodic_table_df):
    cleaned_periodic_table = pd.DataFrame()
    cleaned_periodic_table['atomic_number'] = periodic_table_df[
        'Atomic Number']
    cleaned_periodic_table['atomic_weight'] = periodic_table_df[
        'Atomic Weight'].apply(atomic_weight_clean)
    cleaned_periodic_table['density'] = periodic_table_df.Density.apply(
        density_clean)
    cleaned_periodic_table['phase'] = periodic_table_df['Phase']
    cleaned_periodic_table['melting_point'] = periodic_table_df[
        'Melting Point'].apply(temp_point_clean)
    cleaned_periodic_table['boiling_point'] = periodic_table_df[
        'Boiling Point'].apply(temp_point_clean)
    # cleaned_periodic_table['absolute_melting_point'] =
    # periodic_table_df['Absolute Melting Point'].apply(temp_point_clean)
    # cleaned_periodic_table['absolute_boiling_point'] =
    # periodic_table_df['Absolute Boiling Point'].apply(temp_point_clean)
    cleaned_periodic_table['critical_temperature'] = periodic_table_df[
        'Critical Temperature'].apply(temp_point_clean)
    cleaned_periodic_table['critical_pressure'] = periodic_table_df[
        'Critical Pressure'].apply(pressure_clean, v='MPa')
    cleaned_periodic_table['heat_of_fusion'] = periodic_table_df[
        'Heat of Fusion'].apply(heat_clean)
    cleaned_periodic_table['heat_of_vaporization'] = periodic_table_df[
        'Heat of Vaporization'].apply(heat_clean)
    cleaned_periodic_table['specific_heat'] = periodic_table_df[
        'Specific Heat'].apply(specific_heat_clean)
    cleaned_periodic_table['adiabatic_index'] = periodic_table_df[
        'Adiabatic Index'].apply(adiabatic_index_clean)
    cleaned_periodic_table['neel_point'] = periodic_table_df[
        'Neel Point'].apply(temp_point_clean)
    cleaned_periodic_table['thermal_conductivity'] = periodic_table_df[
        'Thermal Conductivity'].apply(thermal_conductivity_clean)
    cleaned_periodic_table['thermal_expansion'] = periodic_table_df[
        'Thermal Expansion'].apply(thermal_expansion_clean)
    cleaned_periodic_table['density__liquid'] = periodic_table_df[
        'Density (Liquid)'].apply(density_clean)
    cleaned_periodic_table['molar_volume'] = periodic_table_df[
        'Molar Volume'].apply(molar_volume_clean)
    cleaned_periodic_table['brinell_hardness'] = periodic_table_df[
        'Brinell Hardness'].apply(pressure_clean)
    cleaned_periodic_table['mohs_hardness'] = periodic_table_df[
        'Mohs Hardness'].apply(coef_clean)
    cleaned_periodic_table['vickers_hardness'] = periodic_table_df[
        'Vickers Hardness'].apply(pressure_clean)
    cleaned_periodic_table['bulk_modulus'] = periodic_table_df[
        'Bulk Modulus'].apply(pressure_clean, v='GPa')
    cleaned_periodic_table['shear_modulus'] = periodic_table_df[
        'Shear Modulus'].apply(pressure_clean, v='GPa')
    cleaned_periodic_table['young_modulus'] = periodic_table_df[
        'Young Modulus'].apply(pressure_clean, v='GPa')
    cleaned_periodic_table['poisson_ratio'] = periodic_table_df[
        'Poisson Ratio'].apply(coef_clean)
    cleaned_periodic_table['refractive_index'] = periodic_table_df[
        'Refractive Index'].apply(coef_clean)
    cleaned_periodic_table['refractive_index'] = periodic_table_df[
        'Refractive Index'].apply(coef_clean)
    cleaned_periodic_table['speed_sound'] = periodic_table_df[
        'Speed of Sound'].apply(speed_clean)
    cleaned_periodic_table['valence'] = periodic_table_df['Valence'].apply(
        coef_clean)
    cleaned_periodic_table['electronegativity'] = periodic_table_df[
        'Electronegativity'].apply(coef_clean)
    cleaned_periodic_table['electron_affinity'] = periodic_table_df[
        'ElectronAffinity'].apply(heat_clean)
    cleaned_periodic_table['color'] = periodic_table_df['Color']
    cleaned_periodic_table['electrical_conductivity'] = periodic_table_df[
        'Electrical Conductivity'].apply(conductivity_clean)
    cleaned_periodic_table['electrical_resistivity'] = periodic_table_df[
        'Resistivity'].apply(resistivity_clean)
    cleaned_periodic_table['superconducting_point'] = periodic_table_df[
        'Superconducting Point'].apply(coef_clean)
    cleaned_periodic_table['curie_point'] = periodic_table_df[
        'Curie Point'].apply(temp_point_clean)
    cleaned_periodic_table['volume_magnetic_susceptibility'] = \
        periodic_table_df['Volume Magnetic Susceptibility'].apply(coef_clean)
    cleaned_periodic_table['atomic_radius'] = periodic_table_df[
        'Atomic Radius'].apply(radius_clean)
    cleaned_periodic_table['covalent_radius'] = periodic_table_df[
        'Covalent Radius'].apply(radius_clean)
    cleaned_periodic_table['van_der_waals_radius'] = periodic_table_df[
        'Van der Waals Radius'].apply(radius_clean)
    cleaned_periodic_table['lattice_constants__1'] = periodic_table_df[
        'Lattice Constants'].apply(lattice_constants_clean, index=1)
    cleaned_periodic_table['lattice_constants__2'] = periodic_table_df[
        'Lattice Constants'].apply(lattice_constants_clean, index=2)
    cleaned_periodic_table['lattice_constants__3'] = periodic_table_df[
        'Lattice Constants'].apply(lattice_constants_clean, index=3)
    # cleaned_periodic_table['lattice_angles__1'] =
    # periodic_table_df['Lattice Constants'].apply(
    # lattice_constants_clean, index=1)
    # cleaned_periodic_table['lattice_angles__2'] =
    # periodic_table_df['Lattice Constants'].apply(
    # lattice_constants_clean, index=2)
    # cleaned_periodic_table['lattice_angles__3'] =
    # periodic_table_df['Lattice Constants'].apply(
    # lattice_constants_clean, index=3)
    # cleaned_periodic_table['half_life'] =
    # periodic_table_df['Half-Life '].apply(life_clean)
    # cleaned_periodic_table['lifetime'] =
    # periodic_table_df['Lifetime '].apply(life_clean)
    cleaned_periodic_table['decay_mode'] = periodic_table_df['Decay Mode']
    cleaned_periodic_table['neutron_cross_section'] = periodic_table_df[
        'Neutron Cross Section'].apply(coef_clean)
    cleaned_periodic_table['neutron_mass_absorption'] = periodic_table_df[
        'Neutron Mass Absorption'].apply(coef_clean)
    cleaned_periodic_table['isotopic_abundances'] = periodic_table_df[
        'Isotopic Abundances'].apply(isotopic_clean)
    return cleaned_periodic_table


if __name__ == '__main__':
    file_path = os.path.dirname(os.path.abspath(__file__))
    general_path = os.path.join(file_path, '..', '../')
    data_raw_path = os.path.join(general_path, 'data', 'raw')
    data_interim_path = os.path.join(general_path, 'data', 'interim')
    data_raw_filename = os.path.join(data_raw_path, 'data.csv')
    data_interim_filename = os.path.join(data_interim_path, 'clean_data.csv')
    periodic_table_df = read_data_as_csv(data_raw_filename, keep_na=False)
    cleaned_data = clean_periodic_table_df(periodic_table_df)
    save_as_csv(data_interim_filename, cleaned_data)
