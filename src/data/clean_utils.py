from numpy import nan


def cientific_notation_deal(value):
    real_value = value
    if '×' in value:
        coef, power = value.split('×10')
        real_value = float(coef) * 10 ** float(power)
    return str(real_value)


def note_deal(value):
    value = value.replace('[note]', '')
    return value


def atomic_weight_clean(atom_w):
    atom_w = note_deal(atom_w)
    atom_w_f = float(atom_w)
    return atom_w_f


def density_clean(density):
    density = note_deal(density)
    if density == 'N/A':
        return nan
    val, unit = density.split(' ')
    val = float(val)
    if unit == 'g/l':
        val = val * (1 / 1000)
    return val


def temp_point_clean(temp):
    temp = note_deal(temp)
    if temp == 'N/A':
        return nan
    val, unit = temp.split(' ')
    val = float(val)
    if unit == '°C':
        val = val + 273.15
    return val


def pressure_clean(pressure, v='MPa'):
    pressure = note_deal(pressure)
    if pressure == 'N/A':
        return nan
    val, unit = pressure.split(f' {v}')
    val = float(val)
    return val


def heat_clean(heat):
    heat = note_deal(heat)
    if heat == 'N/A':
        return nan
    val, unit = heat.split(' kJ/mol')
    val = float(val)
    return val


def specific_heat_clean(spec_heat):
    spec_heat = note_deal(spec_heat)
    if spec_heat == 'N/A':
        return nan
    val, unit = spec_heat.split(' J/(kg K)')
    val = float(val)
    return val


def adiabatic_index_clean(ai):
    ai = note_deal(ai)
    if ai == 'N/A':
        return nan
    cp, cv = ai.split('/')
    cp, cv = float(cp), float(cv)
    return cp / cv


def thermal_conductivity_clean(tc):
    tc = tc.replace('[note]', '')
    if tc == 'N/A':
        return nan
    val, unit = tc.split(' W/(m K)')
    val = float(val)
    return val


def thermal_expansion_clean(thermal_exp):
    thermal_exp = note_deal(thermal_exp)
    if thermal_exp == 'N/A':
        return nan
    val, unit = thermal_exp.split(' K-1')
    val = float(cientific_notation_deal(val))
    return val


def molar_volume_clean(mv):
    mv = note_deal(mv)
    if mv == 'N/A':
        return nan
    val = float(cientific_notation_deal(mv))
    return val


def speed_clean(speed):
    speed = note_deal(speed)
    if speed == 'N/A':
        return nan
    val, unit = speed.split(' m/s')
    val = float(val)
    return val


def coef_clean(coef):
    coef = note_deal(coef)
    if coef == 'N/A':
        return nan
    val = float(cientific_notation_deal(coef))
    return val


def conductivity_clean(cond):
    cond = note_deal(cond)
    if cond == 'N/A':
        return nan
    val, unit = cond.split(' S/m')
    val = float(cientific_notation_deal(val))
    return val


def resistivity_clean(cond):
    cond = note_deal(cond)
    if cond == 'N/A':
        return nan
    val, unit = cond.split(' m Ω')
    val = float(cientific_notation_deal(val))
    return val


def radius_clean(radius):
    radius = note_deal(radius)
    if radius == 'N/A':
        return nan
    val, unit = radius.split(' pm')
    val = float(cientific_notation_deal(val))
    return val


def lattice_constants_clean(values, index=0):
    index = index - 1
    values = note_deal(values)
    if values == 'N/A':
        return nan
    c_values, unit = values.split(' pm')
    val = c_values.split(',')[index]
    return val


def isotopic_clean(iso):
    vals = iso.count('%')
    return vals


def life_clean():
    pass
