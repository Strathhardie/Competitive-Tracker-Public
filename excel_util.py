import win32com.client as win32
import sys, os, json, zipfile

def exportModules(wb, app):
	try:
		print("Exporting excel modules...", end=" ")
		app.Run('ExportSourceFiles')
		print("Done.")
	except Exception as e:
		print("Error.")
		print(e)

def importModules(wb, app):
	try:
		print("Importing excel modules...", end=" ")
		app.Run('ImportSourceFiles')
		wb.Save()
		print("Done.")
	except Exception as e:
		print("Error.")
		print(e)

def unzip():
	try:
		print("Unzipping excel file...", end=" ")
		with zipfile.ZipFile(args['workbook_path'], 'r') as zip_ref:
			zip_ref.extractall(args['dump_path'])
		print("Done.")
	except Exception as e:
		print("Error.")

def getArgs():
	try:
		with open(os.path.join(os.path.dirname(__file__), 'excel_util_config.json'), 'r') as file:
			return json.load(file)
	except Exception as e:
		print("Error config file missing.")
		print(e)
	return {}

###############################################

try:
	args = getArgs()
	excel = win32.gencache.EnsureDispatch('Excel.Application')
	wb = excel.Workbooks.Open(args['workbook_path'])
	excel.Visible = args['visible'] == "true"

	if len(sys.argv) < 2:
		print('Error: no argument provided.')
	elif sys.argv[1] == "unzip":
		exportModules(wb, excel.Application)
		unzip()
	elif sys.argv[1] == "zip":
		importModules(wb, excel.Application)
	else:
		print('Error: invalid argument \'{}\''.format(sys.argv[1]))

except Exception as e:
	print("Unexpected error.")
	print(e)

# close workbook and excel instance
wb.Close()
excel.Application.Quit()