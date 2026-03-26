' Runs screenshot with no cmd window and does not wait (same as detached start).
' Double-click this file if you want zero console flash; or use screenshot.bat.

Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
baseDir = fso.GetParentFolderName(WScript.ScriptFullName)
q = Chr(34)
pyw = baseDir & "\.venv\Scripts\pythonw.exe"
py = baseDir & "\screenshot.py"
cmdLine = q & pyw & q & " " & q & py & q
Dim i, arg
For i = 0 To WScript.Arguments.Count - 1
  arg = WScript.Arguments(i)
  If InStr(arg, " ") > 0 Then
    cmdLine = cmdLine & " " & q & arg & q
  Else
    cmdLine = cmdLine & " " & arg
  End If
Next
sh.CurrentDirectory = baseDir
sh.Run cmdLine, 0, False
