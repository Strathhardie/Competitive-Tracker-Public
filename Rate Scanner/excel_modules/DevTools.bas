Attribute VB_Name = "DevTools"
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
    
    Debug.Print "Modules exported to './excel_modules'"
End Sub

Public Sub ImportSourceFiles()
    Dim file As String
    Application.ScreenUpdating = False
    Call RemoveAllModules
    file = Dir(ActiveWorkbook.Path + "\excel_modules\")
    While (file <> vbNullString)
        If Not file = "DevTools.bas" Then
            Application.VBE.ActiveVBProject.VBComponents.Import ActiveWorkbook.Path & "\excel_modules\" & file
            'Application.VBE.ActiveVBProject.VBComponents.Import sourcePath & file
        End If
        file = Dir
    Wend
    Application.ScreenUpdating = True
    
    Debug.Print "Modules imported from './excel_modules'"
End Sub

Private Sub RemoveAllModules()
    Dim project As VBProject
    Set project = Application.VBE.ActiveVBProject
    
    Dim comp As VBComponent
    For Each comp In project.VBComponents
        If Not comp.Name = "DevTools" And (comp.Type = vbext_ct_ClassModule Or comp.Type = vbext_ct_StdModule) Then
            project.VBComponents.Remove comp
        End If
    Next
End Sub
 
Private Function ToFileExtension(vbeComponentType As vbext_ComponentType) As String
    'pick file extension based on filetype
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
