VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} Complete 
   ClientHeight    =   945
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   3870
   OleObjectBlob   =   "Complete.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "Complete"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False


Private Sub UserForm_Click()

End Sub

Private Sub UserForm_Initialize()

'Start Userform Centered inside Excel Screen (for dual monitors)
  Me.StartUpPosition = 0
  Me.Left = Application.Left + (0.5 * Application.Width) - (0.5 * Me.Width)
  Me.Top = Application.Top + (0.5 * Application.Height) - (0.5 * Me.Height)

End Sub
