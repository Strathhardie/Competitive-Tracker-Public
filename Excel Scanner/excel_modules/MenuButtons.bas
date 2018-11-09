Attribute VB_Name = "MenuButtons"
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
    
    ' Set variables
    SheetName = "Retail_Report"
    FileName = "Retail Savings - Competitive Review"
    
    ' Archive sheet
    Call ArchiveSheet(SheetName, FileName)
End Sub

Sub ArchiveUS_Click()
    ' Declare variables
    Dim SheetName As String
    Dim FileName As String
    
    ' Set variables
    SheetName = "US$_Report"
    FileName = "US$ - Competitive Review"
    
    ' Archive sheet
    Call ArchiveSheet(SheetName, FileName)
End Sub

Sub ArchiveBroker_Click()
    ' Declare variables
    Dim SheetName As String
    Dim FileName As String
    
    ' Set variables
    SheetName = "Broker_Report"
    FileName = "Broker HISA - Competitive Review"
    
    ' Archive sheet
    Call ArchiveSheet(SheetName, FileName)
End Sub

Sub ArchiveAll_Click()
    Call ArchiveRetail_Click
    Call ArchiveUS_Click
    Call ArchiveBroker_Click
End Sub

Sub RefreshAll_Click()
    Call RefreshQueries
    Call HighlightAllChanges
    MsgBox ("Data refresh completed.")
End Sub

Sub RefreshArchive_Click()
    Call RefreshAll_Click
    Call ArchiveAll_Click
End Sub
