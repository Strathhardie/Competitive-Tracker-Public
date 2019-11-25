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
    Dim i As Integer
    Dim x As Integer
    Dim currTime As Date, execTime As Long
    
    With Worksheets("Menu")
        ' Clear Query Outcome Summary
        Range(.Range("E5"), .Range("E5").End(xlDown).End(xlDown).Offset(0, 5)).ClearContents
        Application.GoTo Reference:=.Range("E3"), scroll:=True
        
        i = 0
        
        ' Iterate through all worksheets containing queries
        For Each wks In Worksheets
            If wks.Name <> "Menu" And _
               wks.Name <> "Retail_Report" And _
               wks.Name <> "US$_Report" And _
               wks.Name <> "Broker_Report" And _
               wks.Name <> "Dev Change Log" Then
               
                On Error GoTo RefreshErrHandler:
            
                    ' Iterate through each query in a worksheet
                    For Each lo In wks.ListObjects
                        x = 1
                        currTime = Now
Context:
                        lo.QueryTable.Refresh
                        execTime = (Now - currTime) * 86400
                        .Range("E5").Offset(i, 0) = i
                        .Range("E5").Offset(i, 1) = lo.Name
                        .Range("E5").Offset(i, 2) = "Success"
                        .Range("E5").Offset(i, 3) = execTime
                        .Range("E5").Offset(i, 4).ClearContents
                        .Range("E5").Offset(i, 5) = x
                        i = i + 1
Point:
                    Next lo
            End If
        Next wks
    End With
    
    Set qt = Nothing
    Set wks = Nothing
    Set lo = Nothing
Exit Sub

' When a QueryTable refresh fails
RefreshErrHandler:
    execTime = (Now - currTime) * 86400
    Range("E5").Offset(i, 0) = i
    Range("E5").Offset(i, 1) = lo.Name
    Range("E5").Offset(i, 2) = "Error"
    Range("E5").Offset(i, 4) = Err.Description
    
    ' Re-run mechanism on error
    Do While x < 4
        Range("E5").Offset(i, 3) = execTime
        Range("E5").Offset(i, 2) = "Retrying"
        Range("E5").Offset(i, 5) = x
        
        Debug.Print lo.Name & " - Attempt " & x & ", " & Err.Description
        
        x = x + 1
        
        Resume Context:
    Loop
    
    i = i + 1
    
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








