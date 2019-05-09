Attribute VB_Name = "RefreshData"
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
    Dim failed() As Variant
    
    
    For Each wks In Worksheets
        
        On Error GoTo RefreshErrHandler:
        
            For Each qt In wks.QueryTables
20              qt.Refresh BackgroundQuery:=False
            Next qt
        
            For Each lo In wks.ListObjects
30                lo.QueryTable.Refresh BackgroundQuery:=False
            Next lo
    
    Next wks

    Set qt = Nothing
    Set wks = Nothing
Exit Sub

RefreshErrHandler:
    If Err.Number = 1004 Then
        
        'TODO Add logging
        'TODO Add to some list of failed queries
        Dim source As String
        Select Case Erl
            Case 20     'Error occurred on qt.Refresh
                source = qt.Name
            Case 30     'Error occurred on lo.QueryTable.Refresh
                source = lo.Name
            Case Else
                source = "unexpected source"
        End Select
            
        MsgBox ("An Error occured while refreshing data for a query in Worksheet '" + wks.Name + "'. Please check rates manually and troubleshoot the tool to fix the error. \n Error Description: " + Err.Description)
        
    Else
        MsgBox ("not error 1004. Error: " + Err.Description)
    End If
    Resume Next 'Continue at line following the one where error was thrown
    
End Sub



'@REVISION HISTORY
'|Date          |Change Author      |Summary of change
'
'|21-09-2018    |Sean R. Smith      |Add Error Handling for failed queries with a continue so that other queries will be attempted.
'
'|30-07-2018    |Jude Arokiam       |Add Refresh All Queries


