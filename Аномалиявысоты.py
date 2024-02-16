from elevation import enter_data, elevation
from helpers.constants import Z7MR5
from patent import get_decimal_degrees
from typing import Dict
from pydantic import BaseModel


class LevellingData(BaseModel):
    H_levelling_m: float


def calc_add_more(levelling: Dict[str, LevellingData], a: str, b: str):
    point1 = a.upper()
    point2 = b.upper()
    datatable = {'decimal_degrees_data': {}, 'rod_temp_corr_baseline': {}, 'misclosure_baseline': {}}
    try:
        data = enter_data(point1 + '_' + point2)
        print('------------------------------------------')
        print(data)
        adj_diff_in_elv, rod_temp_corr_dict, misclosure_dict = elevation(data)
        h_levelling_m = Z7MR5
        if levelling:
            h_levelling_m = levelling[point1].H_levelling_m
        if h_levelling_m == Z7MR5:
            decimal_degrees_data = get_decimal_degrees()
            print('Decimal degree------------------------------------------')
            print(decimal_degrees_data)
            datatable['decimal_degrees_data']['7MR5'] = decimal_degrees_data.get('7MR5', None)
            # decimal_degrees for table
            if point1 not in levelling:
                levelling[point1] = {'H_levelling_m': h_levelling_m}
            rod_temp_corr_baseline = rod_temp_corr_dict.get('Rod Temp Corr Baseline', None)
            misclosure_baseline = misclosure_dict.get('Misclosure Baseline', None)
            datatable['rod_temp_corr_baseline'][point1] = rod_temp_corr_baseline
            datatable['misclosure_baseline'][point1] = misclosure_baseline
        if point2 not in levelling:
            levelling[point2] = {'H_levelling_m': h_levelling_m - adj_diff_in_elv}
        rod_temp_corr_baseline = rod_temp_corr_dict.get('Rod Temp Corr Baseline', None)
        misclosure_baseline = misclosure_dict.get('Misclosure Baseline', None)
        decimal_degrees_data = get_decimal_degrees()
        datatable['decimal_degrees_data'][point2] = decimal_degrees_data.get(point2, None)
        datatable['rod_temp_corr_baseline'][point2] = rod_temp_corr_baseline
        datatable['misclosure_baseline'][point2] = misclosure_baseline
        datatable['levelling'] = levelling

        return datatable
    except Exception as e:
        print(str(e))
        return str(e)
