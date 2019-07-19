' @author: Jude Arokiam
' @date: July 26, 2018
' @version: 2.0
'
' PURPOSE:
' All UI related code should be place in this module.
' Button clicks have been mapped the following procedures.

Option Explicit

Sub ArchiveRetail_Click()
    ' Declare variables
    Dim SheetName As String
    Dim FileName As String
    
    Application.ScreenUpdating = False
    
    ' Set variables
    SheetName = "Retail_Report"
    FileName = "Retail Savings - Competitive Review"
    
    ' Archive sheet
    Call ArchiveSheet(SheetName, FileName)
    
    Application.ScreenUpdating = True
End Sub

Sub ArchiveUS_Click()
    ' Declare variables
    Dim SheetName As String
    Dim FileName As String
    
    Application.ScreenUpdating = False
    
    ' Set variables
    SheetName = "US$_Report"
    FileName = "US$ - Competitive Review"
    
    ' Archive sheet
    Call ArchiveSheet(SheetName, FileName)
    
    Application.ScreenUpdating = True
End Sub

Sub ArchiveBroker_Click()
    ' Declare variables
    Dim SheetName As String
    Dim FileName As String
    
    Application.ScreenUpdating = False
    
    ' Set variables
    SheetName = "Broker_Report"
    FileName = "Broker HISA - Competitive Review"
    
    ' Archive sheet
    Call ArchiveSheet(SheetName, FileName)
    
    Application.ScreenUpdating = True
End Sub

Sub ArchiveAll_Click()
    Call ArchiveRetail_Click
    Call ArchiveUS_Click
    Call ArchiveBroker_Click
    MsgBox ("Report exporting completed.")
End Sub

Sub RefreshAll_Click()
    Call RefreshQueries
    Call HighlightAllChanges
    Dim execTime As Integer
    execTime = Application.WorksheetFunction.Sum(Range(Worksheets("Menu").Range("H5"), Worksheets("Menu").Range("H5").End(xlDown)))
    MsgBox ("Data refresh completed. Total execution time was " & execTime & " seconds.")
<<<<<<< HEAD
=======
    ActiveWorkbook.Save
>>>>>>> efa360a8fc04762431a97390ebc0cbe5d841506d
End Sub

Sub RefreshArchive_Click()
    Call RefreshAll_Click
    Call ArchiveAll_Click
End Sub
