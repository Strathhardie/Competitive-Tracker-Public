import pandas as pd
from styleframe import StyleFrame, Styler, utils

from API.Brokerage import merged_brokerage_rates, mappings as brokerage_map
from API.Retail import merged_retail_rates, mappings as retail_map
from API.USD import merged_usd_rates, mappings as usd_map


# Adds + symbol to complex objects indicating Base rates and added Bonus rates
def normalize_nested_json(data):
    for key in data.keys():
        values = data[key]
        if any(isinstance(i, list) for i in values):
            data[key] = [" + ".join(map(str, value)) if isinstance(value, list) else value for value in values]
    return data


def main():
    writer = StyleFrame.ExcelWriter('RateScanner.xlsx')

    default_style = Styler(font=utils.fonts.calibri)
    header_style = Styler(bold=True, font=utils.fonts.arial, font_size=10)

    for (k, v, m) in [('Retail', merged_retail_rates(), retail_map()),
                      ('USD', merged_usd_rates(), usd_map()),
                      ('Brokerage', merged_brokerage_rates(), brokerage_map())]:
        df = pd.DataFrame(normalize_nested_json(v)).loc[::-1]
        df = df.rename(columns={
            code['acc_code']: '=HYPERLINK("%s", "%s\n%s")' % (code['url'], code['institution'], code['account_name'])
            for code in m})
        sf = StyleFrame(df, styler_obj=default_style)
        sf.apply_headers_style(styler_obj=header_style)

        #Get the max length of each column
        max_len_dict = dict(
            [(v, df[v].apply(lambda r: len(str(r)) if r != None else 0).max()) for v in df.columns.values])

        #Set minimum column width to 12 units
        min_12 = lambda v: v if v > 12 else 12
        max_len_dict = {k: min_12(v) for k, v in max_len_dict.items()}

        # Change the columns width and the rows height
        sf.set_column_width_dict(col_width_dict=max_len_dict)
        all_rows = sf.row_indexes
        sf.set_row_height_dict(row_height_dict={
            all_rows[0]: 90,  # headers row
            all_rows[1:]: 15
        })
        sf.to_excel(excel_writer=writer, sheet_name=k).save()


if __name__ == "__main__":
    main()
