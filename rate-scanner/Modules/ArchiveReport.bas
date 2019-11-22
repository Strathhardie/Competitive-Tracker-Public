Attribute VB_Name = "ArchiveReport"
' @author: Jude Arokiam
' @date: July 26, 2018
' @version: 2.0
'
' PURPOSE:
' Archive Competitive Review Reports to folder. Each archive will append date and time.

Option Explicit

' Copy specified sheet to a new workbook and save under Archive folder.
' The date and time will be appended to the new file created.
' Example Output: Broker HISA - Competitive Review_20180726-15:21
'
' @param sheetName The name of the sheet. e.g "Sheet1"
'                  (NOTE: this is not the text name seen at bottom of sheets)
' @param fileName  The name of the file.  e.g "Broker HISA - Competitive Review"
Sub ArchiveSheet(SheetName As String, FileName As String)
    'Declare variables
    Dim wb As Workbook
    Dim outputPath As String
    Dim FilePath As String
    Dim dateTimeStamp As String
    
    ' Set variables
    On Error GoTo FileErrHandler:
    Set wb = Workbooks.Add
    outputPath = Application.ThisWorkbook.Path & "\Archive"
    dateTimeStamp = GetDateTimeStamp()
    FilePath = outputPath & "\" & FileName & "_" & dateTimeStamp & ".xlsx"
    
    ' Create Archive folder if it does not exist
    If Len(Dir(outputPath, vbDirectory)) = 0 Then
        MkDir outputPath
    End If
    
    ' Copy sheet to new workbook
    ThisWorkbook.Sheets(SheetName).Copy Before:=wb.Sheets(1)
    wb.SaveAs FilePath
    wb.Close Savechanges:=True

Exit Sub

FileErrHandler:
 MsgBox Err.Description

End Sub

' Output date and time
'
' @return string of datetime with expected format
Function GetDateTimeStamp()
    ' Declare Variables
    Dim dateTime As Date

    ' Set Variables
    dateTime = Now()
    
    ' Return formatted date and time
    GetDateTimeStamp = Format(dateTime, "yyyymmdd-hhmm")
End Function

'@REVISION HISTORY
'|Date          |Change Author      |Summary of change
'


