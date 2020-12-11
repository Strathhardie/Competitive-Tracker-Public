import glob
import os
import xlsxwriter
import pandas as pd
from pathlib import Path
from datetime import date


    


def compare_changed_Special_Offer():



    #Today date in order to generate Excel timestamp
    todayDate = str(date.today())

    #Get correct file
    excelFile=glob.glob("specialOffer_[0-9]*.xlsx")
    excelFile = sorted(excelFile)

    #path to files
    currentDirectory = os.getcwd()+"\\"
    path_OLD=Path(currentDirectory+excelFile[len(excelFile)-2])
    path_NEW=Path(currentDirectory+excelFile[len(excelFile)-1])



    # Read in the two excel files and fill NA
    df_OLD = pd.read_excel(path_OLD,header=None, names=None).fillna(0)
    df_NEW = pd.read_excel(path_NEW,header=None, names=None).fillna(0)


    dfDiff = df_OLD.copy()
    for row in range(dfDiff.shape[0]):
        for col in range(dfDiff.shape[1]):
            value_OLD = df_OLD.iloc[row,col]
            try:
                value_NEW = df_NEW.iloc[row,col]
                if value_OLD==value_NEW and value_NEW!=0:
                    dfDiff.iloc[row,col] = df_NEW.iloc[row,col]
                    print(df_NEW.iloc[row,col])
                elif value_OLD==value_NEW and value_NEW==0:
                    dfDiff.iloc[row,col] = ""
                elif( value_OLD!=value_NEW and value_NEW==0):
                    dfDiff.iloc[row,col] = ('Expired Offers: {}').format(value_OLD)
                else:
                    dfDiff.iloc[row,col] = ('Update To: {}').format(value_NEW)

            except:
                dfDiff.iloc[row,col] = ('{}-->{}').format(value_OLD, 'NaN')
    writer = pd.ExcelWriter("specialOffer_compare"+todayDate+".xlsx", engine='xlsxwriter') # pylint: disable=abstract-class-instantiated
    dfDiff.to_excel(writer, sheet_name='DIFF', index=False, header=None)




    workbook  = writer.book
    worksheet = writer.sheets['DIFF']


    # define formats
    highlight_fmt_red = workbook.add_format({'font_color': '#000000', 'bg_color':'#FF0000'})
    highlight_fmt_yellow = workbook.add_format({'font_color': '#000000', 'bg_color':'#FFFF00'})

    ## highlight Update cells
    worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                            'criteria': 'containing',
                                            'value':'Update To',
                                            'format': highlight_fmt_yellow})
    ## highlight Expired cells
    worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                            'criteria': 'containing',
                                            'value':'Expired Offers',
                                            'format': highlight_fmt_red})
    
    # Style Excel Format

    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1})
    worksheet.set_row(0, None, header_format)

    # Add a first row "Bank" format.
    first_column_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        # 'valign': 'center',
        'align': 'center', 
        'valign': 'vcenter',
        # 'fg_color': '#D7E4BC',
        'border': 1})
    worksheet.set_column('A:A', 20, first_column_format)


    # save
    writer.save()