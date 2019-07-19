' @author: Jude Arokiam
' @date: July 30, 2018
' @Revision: 3
' **Revision history at end of script
'
' PURPOSE:
' Refresh all queries.
' Source: https://stackoverflow.com/questions/31476040/refresh-all-queries-in-workbook

Option Explicit
Option Private Module

Public Sub RefreshQueries()
    ' Declare variables
    Dim wks As Worksheet
    Dim qt As QueryTable
    Dim lo As ListObject
    'Dim failed() As Variant
    'Dim success() As Variant
    Dim i As Integer
    Dim count As Integer
    Dim currTime As Date, execTime As Long
    
    
    Range(Range("E5"), Range("E5").End(xlDown).End(xlDown).Offset(0, 4)).ClearContents
    'Cells(4, 5) = "Number"
    'Cells(4, 6) = "Table Name"
    'Cells(4, 7) = "Status"
    'Cells(4, 8) = "Execution Time"
    'Cells(4, 9) = "Message"
    'Cells(3, 5) = "Query Outcome Summary"
    count = 0
    Application.GoTo Reference:=Worksheets("Menu").Range("E3"), scroll:=True
    
    i = 0
    For Each wks In Worksheets
        If wks.Name <> "Menu" And _
           wks.Name <> "Retail_Report" And _
           wks.Name <> "US$_Report" And _
           wks.Name <> "Broker_Report" And _
           wks.Name <> "BNS_Rates" And _
           wks.Name <> "Dev Change Log" Then
           
'        On Error GoTo RefreshErrHandler:
'            For Each qt In wks.QueryTables
'20              qt.Refresh BackgroundQuery:=False
'                ' Range("E5").Offset(i, 2) = qt.Name
'
'            Next qt
        
        On Error GoTo RefreshErrHandler:
        
            For Each lo In wks.ListObjects
                  currTime = Now
                  lo.QueryTable.Refresh BackgroundQuery:=False
                  execTime = (Now - currTime) * 86400
                  Range("E5").Offset(i, 0) = i
                  'Range("E5").Offset(i, 0) = lo.QueryTable.Connection
                  Range("E5").Offset(i, 1) = lo.Name
                  Range("E5").Offset(i, 2) = "Success"
                  Range("E5").Offset(i, 3) = execTime
                  'Range(Range("E5").Offset(i, 0), Range("E5").Offset(i, 4)).Show
                  'Application.Goto Reference:=Worksheets("Menu").Range("E5").Offset(i, 0), scroll:=True
                  i = i + 1
Point:
            Next lo
        End If
    Next wks
    
    Set qt = Nothing
    Set wks = Nothing
    Set lo = Nothing
    Debug.Print count
    
Exit Sub

RefreshErrHandler:
    execTime = (Now - currTime) * 86400
    Range("E5").Offset(i, 0) = i
    Range("E5").Offset(i, 1) = lo.Name
    Range("E5").Offset(i, 2) = "Error"
    Range("E5").Offset(i, 3) = execTime
    Range("E5").Offset(i, 4) = Err.Description
    'Range(Range("E5").Offset(i, 0), Range("E5").Offset(i, 4)).Show
    'Application.Goto Reference:=Worksheets("Menu").Range("E5").Offset(i, 0), scroll:=True
    i = i + 1
    
'    If Err.Number = 1004 Then
'        Range("E5").Offset(i, 0) = i
'        Range("E5").Offset(i, 1) = lo.Name
'        Range("E5").Offset(i, 2) = "Error"
'        Range("E5").Offset(i, 3) = Err.Description
'        i = i + 1
'
'        'TODO Add to some list of failed queries
'        Dim source As String
'        Select Case Erl
'            Case 20     'Error occurred on qt.Refresh
'                source = qt.Name
'            Case 30     'Error occurred on lo.QueryTable.Refresh
'                source = lo.Name
'            Case Else
'                source = "unexpected source"
'        End Select
'
'        MsgBox ("An Error occured while refreshing data for a query in Worksheet '" + wks.Name + "'. Please check rates manually and troubleshoot the tool to fix the error. \n Error Description: " + Err.Description)
'
'    Else
'        MsgBox ("not error 1004. Error: " + Err.Description)
'    End If

    Resume Point: 'Continue at line following the one where error was thrown
    
End Sub

Function TimeDiff(startTime As Date, stopTime As Date)
    TimeDiff = Abs(stopTime - startTime) * 86400
End Function

Sub SaveCloseReOpen()
    ThisWorkbook.Save
    Application.Workbooks.Open (ThisWorkbook.FullName)
End Sub

'@REVISION HISTORY
'|Date          |Change Author      |Summary of change
'
'|21-09-2018    |Sean R. Smith      |Add Error Handling for failed queries with a continue so that other queries will be attempted.
'
'|30-07-2018    |Jude Arokiam       |Add Refresh All Queries

'|23-04-2019    |Jacob Bourdeau     |Add logging of query results to menu page






