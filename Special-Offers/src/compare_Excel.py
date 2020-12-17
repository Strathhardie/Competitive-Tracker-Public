import glob
import os
import xlsxwriter
import pandas as pd
from pathlib import Path
from datetime import date

def write_Sav_Che_Sheet(df_OLD,df_NEW):
    dfDiff = df_OLD.copy()
    for row in range(dfDiff.shape[0]):
        for col in range(dfDiff.shape[1]):
            value_OLD = df_OLD.iloc[row,col]
            try:
                value_NEW = df_NEW.iloc[row,col]
                if value_OLD==value_NEW and value_NEW!=0:
                    dfDiff.iloc[row,col] = df_NEW.iloc[row,col]
                elif value_OLD==value_NEW and value_NEW==0:
                    dfDiff.iloc[row,col] = ""
                elif( value_OLD!=value_NEW and value_NEW==0):
                    dfDiff.iloc[row,col] = ('Expired Offers:\n{}').format(value_OLD)
                else:
                    dfDiff.iloc[row,col] = ('Update To:\n{}').format(value_NEW)
                   
            except:
                dfDiff.iloc[row,col] = ('{}-->{}').format(value_OLD, 'NaN')

    for row in range(dfDiff.shape[0]):
        for col in range(dfDiff.shape[1]):
            if row >0 and col ==7:
                if len(dfDiff.iloc[row, col]) <= 255:
                    dfDiff.iloc[row, col] = '=HYPERLINK("{0}","{1}")'.format(dfDiff.iloc[row, col],dfDiff.iloc[row, 0])

    print(dfDiff)
    return dfDiff
    
def write_style_sheet(writer, SavOrCheSheet):
    workbook  = writer.book
    worksheet = writer.sheets[SavOrCheSheet]


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
    header_format_blank = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'align': 'center', 
        'fg_color': '#FFFFFF',
        'border': 1})
    worksheet.set_column("I:Z", None, header_format_blank)

    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'align': 'center', 
        'fg_color': '#D7E4BC',
        'border': 1})
    worksheet.set_row(0, None, header_format)

    # Add a first row "Bank" format.
    first_column_format = workbook.add_format({
        'bold': False,
        'text_wrap': True,
        'align': 'center', 
        'valign': 'vcenter',
        'border': 1})
    worksheet.set_column('A:A', 15, first_column_format)

    # Add a second row "Account Name" format.
    second_column_format = workbook.add_format({
        'bold': False,
        'text_wrap': True,
        'align': 'center', 
        'valign': 'vcenter',
        'border': 1})
    worksheet.set_column('B:B', 50, second_column_format)

    # Add a third row "Account Type" format.
    third_column_format = workbook.add_format({
        'bold': False,
        'text_wrap': True,
        'align': 'center', 
        'valign': 'vcenter',
        'border': 1})
    worksheet.set_column('C:C', 25, third_column_format)

    # Add a forth row "Monthly Fee" format.
    forth_column_format = workbook.add_format({
        'bold': False,
        'text_wrap': True,
        'align': 'left', 
        'valign': 'vcenter',
        'border': 1})
    worksheet.set_column('D:D', 50, forth_column_format)

    # Add a fifth row "Special Offer" format.
    fifth_column_format = workbook.add_format({
        'bold': False,
        'text_wrap': True,
        'align': 'left', 
        'valign': 'vcenter',
        'border': 1})
    worksheet.set_column('E:E', 50, fifth_column_format)

    # Add a sixth row "Expiry Date" format.
    sixth_column_format = workbook.add_format({
        'bold': False,
        'text_wrap': True,
        'align': 'left', 
        'valign': 'vcenter',
        'border': 1})
    worksheet.set_column('F:F', 15, sixth_column_format)

    # Add a seventh row "Account Perks" format.
    seventh_column_format = workbook.add_format({
        'bold': False,
        'text_wrap': True,
        'align': 'left', 
        'valign': 'vcenter',
        'border': 1})
    worksheet.set_column('G:G', 50, seventh_column_format)    

    # Add a eighth row "Webiste" format.
    ninth_column_format = workbook.add_format({
        'bold': False,
        'text_wrap': True,
        'align': 'center', 
        'valign': 'vcenter',
        'border': 1})
    worksheet.set_column('H:H', 30, ninth_column_format)   

    # Freeze the first row.
    worksheet.freeze_panes(1, 0) 



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
    df_OLD_Sav = pd.read_excel(path_OLD,sheet_name="Saving", header=None, names=None).fillna(0)
    df_NEW_Sav = pd.read_excel(path_NEW,sheet_name="Saving",header=None, names=None).fillna(0)
    df_OLD_Che = pd.read_excel(path_OLD,sheet_name="Chequing",header=None, names=None).fillna(0)
    df_NEW_Che = pd.read_excel(path_NEW,sheet_name="Chequing",header=None, names=None).fillna(0)


    writer = pd.ExcelWriter("specialOffer_compare"+todayDate+".xlsx", engine='xlsxwriter') # pylint: disable=abstract-class-instantiated

    write_Sav_Che_Sheet(df_OLD_Sav,df_NEW_Sav).to_excel(writer, sheet_name='DIFF_Sav', index=False, header=None)
    write_Sav_Che_Sheet(df_OLD_Che,df_NEW_Che).to_excel(writer, sheet_name='DIFF_Che', index=False, header=None)


   

    write_style_sheet(writer, "DIFF_Sav")
    write_style_sheet(writer, "DIFF_Che")

    # save
    writer.save()