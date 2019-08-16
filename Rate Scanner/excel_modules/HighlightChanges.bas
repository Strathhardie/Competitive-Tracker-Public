Attribute VB_Name = "HighlightChanges"
' @author: David Yan
' @date: 2018/08/10
' @version: 2.0
'
' PURPOSE:
' To check if the interest rates has changed in each cell.
' If changed, highlight the cell that has changed.
'
' Notable Limitations:
' Only checks for the first 104 columns and 1000 rows
' If expansion is required, please do so in the RangeToExtract value and any relevant range values

Option Explicit

Public Sub HighlightAllChanges()
    'Declare variables
    Dim retailSheetName As String
    Dim retailFilename As String
    Dim usSheetName As String
    Dim usFilename As String
    Dim brokerSheetName As String
    Dim brokerFilename As String
    
    On Error GoTo GenericErrHandler:
    'Define variables
    retailSheetName = "Retail_Report"
    retailFilename = "Retail Savings - Competitive Tracker"
    usSheetName = "US$_Report"
    usFilename = "US$ - Competitive Tracker"
    brokerSheetName = "Broker_Report"
    brokerFilename = "Broker HISA - Competitive Tracker"

    ' Clear previous highlighting for all 3 reports
    Call ResetHighlight(retailSheetName)
    Call ResetHighlight(usSheetName)
    Call ResetHighlight(brokerSheetName)
    
    ' Highlight new changes for all 3 reports
    Call HighlightChange(retailSheetName, retailFilename)
    Call HighlightChange(usSheetName, usFilename)
    Call HighlightChange(brokerSheetName, brokerFilename)
Exit Sub

GenericErrHandler:
MsgBox Err.Description

End Sub

' This function extracts data from the latest archives
' Returns a large varaint array to compare and highlight
' Helper function for highlighting changes
Private Function ExtractArchiveData(SheetName As String, FileName As String) As Variant
' Declare variables
    Dim FilePath As String
    Dim MostRecentFile As String
    Dim MostRecentDate As Date
    Dim oFSO As Object
    Dim oFolder As Object
    Dim oFiles As Object
    Dim oFile As Object
    Dim RangeToExtract As String
    Dim ArchivedBook As Workbook
    
     On Error GoTo GenericErrHandler:
' Set variables and create file system object
    Let RangeToExtract = "A1:DA1000"
    Let FilePath = Application.ThisWorkbook.Path & "\Archive\"
    Set oFSO = CreateObject("Scripting.FileSystemObject")
    Set oFolder = oFSO.GetFolder(FilePath)
    Set oFiles = oFolder.Files
    
    
    Debug.Print FileName
    
' For each file in the archive folder
' If the file's name is the specified name, and time file was modified was more recent than record
' Set that file's date to be most recent date, and record file name
    For Each oFile In oFiles
        If InStr(1, oFile.Name, FileName) = 1 Then
            If FileDateTime(oFile.Path) > MostRecentDate Then
                MostRecentDate = FileDateTime(oFile.Path)
                MostRecentFile = oFile.Path
            End If
                Debug.Print oFile.Name
        End If
                Debug.Print oFile.Name
                'Debug.Print MostRecentFile
    Next oFile

On Error GoTo FileErrHandler:
' Opens the latest archive and extract the data
    Set ArchivedBook = Workbooks.Open(MostRecentFile)
    Let ExtractArchiveData = ArchivedBook.Worksheets(SheetName).Range(RangeToExtract)
    
' Close workbook
    ArchivedBook.Close Savechanges:=False
    
Exit Function
GenericErrHandler:
MsgBox Err.Description

Exit Function
FileErrHandler:
MsgBox "The files that are necessary to make a comparison with it are not available. Please check if the files has been deleted or moved"

End Function
Private Sub ResetHighlight(SheetName As String)

' Declare variables
    Dim Cell As Range
    Dim RangeToReset As String
    
    On Error GoTo FileErrHandler:
    Let RangeToReset = "A1:DA1000"
    
      
' For all the cells in range A1 to DA1000
' Set highlighting to None
    For Each Cell In ThisWorkbook.Sheets(SheetName).Range(RangeToReset)
    
        If Cell.Interior.ColorIndex = 6 Then
        Cell.Interior.Color = xlNone
        End If
    Next Cell
    
Exit Sub
FileErrHandler:
MsgBox Err.Description

End Sub

Private Sub HighlightChange(SheetName As String, FileName As String)

' Declare variables
    Dim ExtractedData As Variant
    Dim CurrentData As Variant
    Dim RangeToHighlight As String
    Dim iRow As Long
    Dim iCol As Long
    
    On Error GoTo GenericErrHandler:
    ' Set variables
    Let RangeToHighlight = "A1:DA1000"
    Let ExtractedData = ExtractArchiveData(SheetName, FileName)
    Let CurrentData = ThisWorkbook.Sheets(SheetName).Range(RangeToHighlight)
    
      
' Function source: https://stackoverflow.com/questions/5387929/vba-macro-to-compare-all-cells-of-two-excel-files#
' Compares the 2 varaint arrays and highlight any changes
   
    For iRow = LBound(CurrentData, 1) To UBound(CurrentData, 1)
        For iCol = LBound(CurrentData, 2) To UBound(CurrentData, 2)
          On Error GoTo FileErrHandler:
            If CurrentData(iRow, iCol) = ExtractedData(iRow, iCol) Then
                ' Cells are identical.
                ' Do nothing.
            Else
                ' Cells are different.
                ' Code goes here for whatever it is you want to do.
                Let Worksheets(SheetName).Cells(iRow, iCol).Interior.ColorIndex = 6
            End If
        Next iCol
    Next iRow
    
Exit Sub
GenericErrHandler:
MsgBox Err.Description

Exit Sub
FileErrHandler:
MsgBox "Unable to find files that are stored in archive folder. Please check if the files has been deleted or moved"

End Sub

