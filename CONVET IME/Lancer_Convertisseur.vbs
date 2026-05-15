' Lanceur sans fenêtre de console pour l'application GUI
Set objShell = CreateObject("WScript.Shell")
strPythonPath = "D:\DEV\.venv\Scripts\python.exe"
strScriptPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\converter_gui.py"

objShell.Run strPythonPath & " """ & strScriptPath & """", 0, False