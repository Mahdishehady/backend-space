from elevation import enter_data, elevation
from helpers.constants import Z7MR5
from patent import get_decimal_degrees


def calc_add_more(levelling: dict, a: str, b: str):
    point1 = a.upper()
    point2 = b.upper()
    datatable = {}
    try:
        data = enter_data(point1 + '_' + point2)
        adj_diff_in_elv, rod_temp_corr_dict, misclosure_dict = elevation(data)
        h_levelling_m = Z7MR5
        if levelling:
            h_levelling_m = levelling[point1]['H (Levelling) m']
        if point2 not in levelling:
            levelling[point2] = {'H (Levelling) m': h_levelling_m - adj_diff_in_elv}
        if h_levelling_m == Z7MR5:
            decimal_degrees_data = get_decimal_degrees()
            datatable['decimal_degrees_data']['7MR5'] = decimal_degrees_data['7MR5']
            # decimal_degrees for table
            if point1 not in levelling:
                levelling[point1] = {'H (Levelling) m': h_levelling_m}
            rod_temp_corr_baseline = rod_temp_corr_dict['Rod Temp Corr Baseline']
            misclosure_baseline = misclosure_dict['Misclosure Baseline']
            datatable['rod_temp_corr_baseline'][point1] = rod_temp_corr_baseline
            datatable['misclosure_baseline'][point1] = misclosure_baseline
        rod_temp_corr_baseline = rod_temp_corr_dict['Rod Temp Corr Baseline']
        misclosure_baseline = misclosure_dict['Misclosure Baseline']
        decimal_degrees_data = get_decimal_degrees()
        datatable['decimal_degrees_data'][point2] = decimal_degrees_data[point2]
        datatable['rod_temp_corr_baseline'][point2] = rod_temp_corr_baseline
        datatable['misclosure_baseline'][point2] = misclosure_baseline
        datatable['levelling'] = levelling

        return datatable
    except Exception as e:
        print(str(e))
        return str(e)
