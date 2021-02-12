import pandas as pd

from API.Brokerage import merged_brokerage_rates, mappings as brokerage_map
from API.Retail import merged_retail_rates, mappings as retail_map
from API.USD import merged_usd_rates, mappings as usd_map


def normalize_nested_json(data):
    for key in data.keys():
        values = data[key]
        if any(isinstance(i, list) for i in values):
            data[key] = [" + ".join(map(str, value)) if isinstance(value, list) else value for value in values]
    return data


def retail_report(writer):
    # Add a header format.
    header_format = {
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'align': 'centre',
        'fg_color': '#D7E4BC',
        'border': 1}
    workbook = writer.book

    print('Starting Retail')
    retail_rates = merged_retail_rates()
    retail_rates = normalize_nested_json(retail_rates)

    df_retail = pd.DataFrame(retail_rates)
    df_retail = df_retail.loc[::-1]
    df_retail = df_retail.rename(columns={
        code['acc_code']: '=HYPERLINK("%s", "%s\n%s")' % (code['url'], code['institution'], code['account_name']) for
        code in retail_map()})
    df_retail.to_excel(writer, sheet_name='Retail_Report', index=False, header=False, startrow=1)

    worksheet = writer.sheets['Retail_Report']

    # Write the column headers with the defined format.
    for col_num, value in enumerate(df_retail.columns.values):
        worksheet.write(0, col_num, value, workbook.add_format(header_format))

    print('Completed Retail')


def usd_report(writer):
    # Add a header format.
    header_format = {
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'align': 'centre',
        'fg_color': '#D7E4BC',
        'border': 1}
    workbook = writer.book

    print('Starting USD')
    usd_rates = merged_usd_rates()
    usd_rates = normalize_nested_json(usd_rates)

    df_usd = pd.DataFrame(usd_rates)
    df_usd = df_usd.loc[::-1]
    df_usd = df_usd.rename(columns=
                           {code['acc_code']: '=HYPERLINK("%s", "%s\n%s")' % (
                               code['url'], code['institution'], code['account_name']) for code in usd_map()}
                           )
    df_usd.to_excel(writer, sheet_name='USD_Report', index=False, header=False, startrow=1)
    worksheet = writer.sheets['USD_Report']

    # Write the column headers with the defined format.
    for col_num, value in enumerate(df_usd.columns.values):
        worksheet.write(0, col_num, value, workbook.add_format(header_format))

    print('Completed USD')


def brokerage_report(writer):
    # Add a header format.
    header_format = {
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'align': 'centre',
        'fg_color': '#D7E4BC',
        'border': 1}
    workbook = writer.book

    print('Starting Brokerage')
    brokerage_rates = merged_brokerage_rates()
    brokerage_rates = normalize_nested_json(brokerage_rates)

    df_brokerage = pd.DataFrame(brokerage_rates)
    df_brokerage = df_brokerage.loc[::-1]
    df_brokerage = df_brokerage.rename(columns=
                           {code['acc_code']: '=HYPERLINK("%s", "%s\n%s")' % (
                               code['url'], code['institution'], code['account_name']) for code in brokerage_map()}
                           )
    df_brokerage.to_excel(writer, sheet_name='Brokerage_Report', index=False, header=False, startrow=1)
    worksheet = writer.sheets['Brokerage_Report']

    # Write the column headers with the defined format.
    for col_num, value in enumerate(df_brokerage.columns.values):
        worksheet.write(0, col_num, value, workbook.add_format(header_format))
    print('Completed Brokerage')


def main():
    writer = pd.ExcelWriter('./RateScanner.xlsx', engine='xlsxwriter')

    retail_report(writer)

    usd_report(writer)

    brokerage_report(writer)

    writer.save()


if __name__ == "__main__":
    main()
