import numpy as np
import re

from numpy import nan

NON_USABLE_FEATURES = [
    'group_block',
    'atomic_mass',
    'melting_point',
    'boiling_point'
]

LOG_FEATURES = []

PHASE_DICT = {
    'Solid': 0,
    'Gas': 100,
    'Liquid': 25
}

ELECTRON_CONFIGURATION = {
    's': 0,
    'p': 1,
    'd': 2,
    'f': 3,
}


def oxidation_states_nb(val):
    if val is None or val is nan:
        return []
    return len(val.split(','))


def neg_oxidation_states_nb(val):
    if val is None or val is nan:
        return nan
    return val.count('-')


def oxidation_state_operation(val, operation):
    if val is None or val is nan:
        return nan
    val = val.replace('+', '')
    val_list = list(map(int, val.split(',')))
    return operation(val_list)


def step_between_oxidation_states(oxidation_list):
    if len(oxidation_list) == 1:
        return 0
    return np.mean(np.gradient(oxidation_list))


def electron_conf_after_noble_gas_list_operation(val, operation):
    val = val.split('(')[0].strip()
    val_list = val.split(']')[-1].strip()
    return operation(val_list.split(' '))


def electron_conf_last_letter(electron_conf_list):
    last_electron_conf = electron_conf_list[-1]
    return re.findall(r'[a-z]', last_electron_conf)[0]


def electron_conf_highest_letter(electron_conf_list):
    electron_conf_str = ' '.join(electron_conf_list)
    configurations = 'fdps'
    for letter in configurations:
        if letter in electron_conf_str:
            return letter


def electron_conf_last_level(electron_conf_list):
    last_electron_conf = electron_conf_list[-1]
    return int(re.split(r'[a-z]', last_electron_conf)[0])


def electron_conf_last_value(electron_conf_list):
    last_electron_conf = electron_conf_list[-1]
    return int(re.split(r'[a-z]', last_electron_conf)[1])


def state_text_parse(val):
    val = val.replace('Expected to be a ', '').strip()
    return val
