import re
import pandas as pd
from styleframe import StyleFrame, Styler, utils

from API.Brokerage import brokerage_df
from API.Retail import retail_df
from API.USD import usd_df
from API.TFSA import tfsa_df
from API.RRSP import rrsp_df

def main(): 
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('rates.xlsx', engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    brokerage_df().to_excel(writer, sheet_name='Brokerage Accounts')
    retail_df().to_excel(writer, sheet_name='Retail Savings and Chequing')
    usd_df().to_excel(writer, sheet_name='US Dollar Accounts')
    tfsa_df().to_excel(writer, sheet_name='TFSA Accounts')
    rrsp_df().to_excel(writer, sheet_name='RRSP Accounts')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()



if __name__ == "__main__":
    main()
