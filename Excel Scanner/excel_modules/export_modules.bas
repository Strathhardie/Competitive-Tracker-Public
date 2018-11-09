Attribute VB_Name = "export_modules"
Public Sub ExportSourceFiles()
    Dim component As VBComponent
    Dim fdObj As Object
    Application.ScreenUpdating = False
    
    'create modules folder if it doens't exist
    Set fdObj = CreateObject("Scripting.FileSystemObject")
    If Not fdObj.FolderExists(ActiveWorkbook.Path + "\excel_modules") Then
        fdObj.CreateFolder (ActiveWorkbook.Path + "\excel_modules")
    End If
    
    'iterate through all components, export the, with file extensions
    For Each component In Application.VBE.ActiveVBProject.VBComponents
        If component.Type = vbext_ct_ClassModule Or component.Type = vbext_ct_StdModule Then
            component.Export ActiveWorkbook.Path + "\excel_modules\" & component.Name & ToFileExtension(component.Type)
        End If
    Next
    Application.ScreenUpdating = True
    
    MsgBox "Modules exported to './excel_modules'"
End Sub
 
Private Function ToFileExtension(vbeComponentType As vbext_ComponentType) As String
    Select Case vbeComponentType
        Case vbext_ComponentType.vbext_ct_ClassModule
            ToFileExtension = ".cls"
        Case vbext_ComponentType.vbext_ct_StdModule
            ToFileExtension = ".bas"
        Case vbext_ComponentType.vbext_ct_MSForm
            ToFileExtension = ".frm"
        Case vbext_ComponentType.vbext_ct_ActiveXDesigner
        Case vbext_ComponentType.vbext_ct_Document
        Case Else
            ToFileExtension = vbNullString
    End Select
End Function
