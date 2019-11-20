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

Sub RefreshArchive_Click()
    Call RefreshAll_Click
    Call ArchiveAll_Click
End Sub
'registers users click and triggers userform
Sub RefreshAll_Click()
    
        'progress indicator
        UserForm1.Show

End Sub
'called by userform once it has been triggered 
Sub Refresh_progressBar()

    Call RefreshQueries
    Call HighlightAllChanges
    Dim execTime As Integer
    execTime = Application.WorksheetFunction.Sum(Range(Worksheets("Menu").Range("H5"), Worksheets("Menu").Range("H5").End(xlDown)))
   ' MsgBox ("Data refresh completed. Total execution time was " & execTime & " seconds.")
    ProgressBar.Text.Caption = QsComp & "/" & totalQs & " Queries Complete, Total execution time was " & execTime & " seconds."
    ActiveWorkbook.Save
    ActiveSheet.Range("B3").Select
    ActiveWindow.ScrollColumn = 1

End Sub
