import sys
import shutil
import os
import json
import time
import requests
import re
from bs4 import BeautifulSoup as htmlParser
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)


class HomePage(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()
		self.new_mod_window = NewMod()
		self.editorWindow = EasyEditor()

	def init_ui(self):
		self.TitleLab = QtWidgets.QLabel('Welcome to the MC Mod Maker')
		self.TitleLab2 = QtWidgets.QLabel('Would you like to load a mod or start fresh?')
		self.loadButton = QtWidgets.QPushButton('Edit Mod')
		self.newModButton = QtWidgets.QPushButton('New Mod')

		self.homepageLayout()

		self.setWindowTitle('MC Mod Maker')

		self.newModButton.clicked.connect(self.newModBtn_click)
		self.loadButton.clicked.connect(self.loadBtn_click)

		self.show()

	def homepageLayout(self):
		titleHbox = QtWidgets.QHBoxLayout()
		titleHbox.addStretch()
		titleHbox.addWidget(self.TitleLab)
		titleHbox.addStretch()

		title2Hbox = QtWidgets.QHBoxLayout()
		title2Hbox.addStretch()
		title2Hbox.addWidget(self.TitleLab2)
		title2Hbox.addStretch()

		buttonsHbox = QtWidgets.QHBoxLayout()
		buttonsHbox.addStretch()
		buttonsHbox.addWidget(self.loadButton)
		buttonsHbox.addStretch()
		buttonsHbox.addWidget(self.newModButton)
		buttonsHbox.addStretch()

		v_box = QtWidgets.QVBoxLayout()
		v_box.addStretch()
		v_box.addLayout(titleHbox)
		v_box.addStretch()
		v_box.addLayout(title2Hbox)
		v_box.addLayout(buttonsHbox)
		v_box.addStretch()

		self.setLayout(v_box)

	def newModBtn_click(self):
		self.new_mod_window.show()
		self.close()

	def loadBtn_click(self):
		self.editorWindow.show()
		self.close()


class NewMod(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()
		self.setup_mod_window = SetupModWindow()

	def init_ui(self):
		self.TitleLab = QtWidgets.QLabel('Make A New MC 1.14.4 Mod')
		self.TitleLab2 = QtWidgets.QLabel('Enter Info about mod:')
		self.userNameLab = QtWidgets.QLabel('Username:')
		self.userNameLe = QtWidgets.QLineEdit(self)
		self.nameLab = QtWidgets.QLabel('Mod Name:')
		self.nameLe = QtWidgets.QLineEdit(self)
		self.modidLab = QtWidgets.QLabel('ModId:')
		self.modidLe = QtWidgets.QLineEdit(self)
		self.modDirLab = QtWidgets.QLabel('Directory:')
		self.modDirPicker = QtWidgets.QComboBox(self)
		self.modDirPicker.addItem("Select Directory")
		self.submitButton = QtWidgets.QPushButton("Setup Mod")
		self.errorLab = QtWidgets.QLabel('')

		self.newModLayout()

		self.modDirPicker.activated[str].connect(self.pickNewDirectory)
		self.submitButton.clicked.connect(self.startModSetup)

		self.setWindowTitle('MC Mod Maker')

	def newModLayout(self):
		titleHbox = QtWidgets.QHBoxLayout()
		titleHbox.addStretch()
		titleHbox.addWidget(self.TitleLab)
		titleHbox.addStretch()

		title2Hbox = QtWidgets.QHBoxLayout()
		title2Hbox.addStretch()
		title2Hbox.addWidget(self.TitleLab2)
		title2Hbox.addStretch()

		userNameHbox = QtWidgets.QHBoxLayout()
		userNameHbox.addStretch()
		userNameHbox.addWidget(self.userNameLab)
		userNameHbox.addWidget(self.userNameLe)
		userNameHbox.addStretch()

		nameHbox = QtWidgets.QHBoxLayout()
		nameHbox.addStretch()
		nameHbox.addWidget(self.nameLab)
		nameHbox.addWidget(self.nameLe)
		nameHbox.addStretch()

		modidHbox = QtWidgets.QHBoxLayout()
		modidHbox.addStretch()
		modidHbox.addWidget(self.modidLab)
		modidHbox.addWidget(self.modidLe)
		modidHbox.addStretch()

		modDirHbox = QtWidgets.QHBoxLayout()
		modDirHbox.addStretch()
		modDirHbox.addWidget(self.modDirLab)
		modDirHbox.addWidget(self.modDirPicker)
		modDirHbox.addStretch()

		submitBtnHbox = QtWidgets.QHBoxLayout()
		submitBtnHbox.addStretch()
		submitBtnHbox.addWidget(self.submitButton)
		submitBtnHbox.addStretch()

		errorLabHbox = QtWidgets.QHBoxLayout()
		errorLabHbox.addStretch()
		errorLabHbox.addWidget(self.errorLab)
		errorLabHbox.addStretch()

		v_box = QtWidgets.QVBoxLayout()
		v_box.addStretch()
		v_box.addLayout(titleHbox)
		v_box.addStretch()
		v_box.addLayout(title2Hbox)
		v_box.addLayout(userNameHbox)
		v_box.addLayout(nameHbox)
		v_box.addLayout(modidHbox)
		v_box.addLayout(modDirHbox)
		v_box.addLayout(submitBtnHbox)
		v_box.addLayout(errorLabHbox)
		v_box.addStretch()

		self.setLayout(v_box)

	def pickNewDirectory(self, text):
		if text == "Select Directory":
			self.modDirPicker.clear()
			modDir = QtWidgets.QFileDialog.getExistingDirectory()
			self.modDirPicker.addItem(modDir)
			self.modDirPicker.addItem("Select Directory")

	def startModSetup(self):
		self.setup_mod_window.show()
		time.sleep(1)
		wasSuccessful = self.setup_mod_window.setupMod(self.modDirPicker.currentText(), self.nameLe.text(), self.userNameLe.text(), self.modidLe.text())
		if wasSuccessful:
			self.setup_mod_window.close()
			self.close()
		else:
			self.errorLab.setText("Process Failed")
			self.update()


class SetupModWindow(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()
		self.easy_editor_window = EasyEditor()

	def init_ui(self):
		self.TitleLab = QtWidgets.QLabel('Making A New MC 1.14.4 Mod')
		self.progressBar = QtWidgets.QProgressBar(self)
		self.errorLab = QtWidgets.QLabel('')

		self.setupModLayout()

		self.setWindowTitle('MC Mod Maker')

	def setupModLayout(self):
		titleHbox = QtWidgets.QHBoxLayout()
		titleHbox.addStretch()
		titleHbox.addWidget(self.TitleLab)
		titleHbox.addStretch()

		progBarHbox = QtWidgets.QHBoxLayout()
		progBarHbox.addStretch()
		progBarHbox.addWidget(self.progressBar)
		progBarHbox.addStretch()

		errorLabHbox = QtWidgets.QHBoxLayout()
		errorLabHbox.addStretch()
		errorLabHbox.addWidget(self.errorLab)
		errorLabHbox.addStretch()

		v_box = QtWidgets.QVBoxLayout()
		v_box.addStretch()
		v_box.addLayout(titleHbox)
		v_box.addStretch()
		v_box.addLayout(progBarHbox)
		v_box.addLayout(errorLabHbox)
		v_box.addStretch()

		self.setLayout(v_box)

	def setupMod(self, modDir, modName, userName, modID):
		self.show()
		newDir = modDir + "/" + modName
		self.errorLab.setText("Creating Mod")
		self.progressBar.setValue((1 / 9) * 100)
		self.update()
		time.sleep(0.5)
		try:
		#if True:
			mcpBot = requests.get("http://export.mcpbot.bspk.rs")
			mcpBotHTML = htmlParser(mcpBot.text, 'html.parser')
			snapshotNames = mcpBotHTML.find_all('td', attrs={"class":"name"})
			latestMcpSnapshot = re.search('mcp_snapshot-(.+?).zip', str(snapshotNames[0])).group(1)
			self.progressBar.setValue((2 / 9) * 100)
			self.update()
			time.sleep(0.5)
			shutil.copytree("LatestMDK", newDir)
			os.chdir(newDir)
			with open("gradle.properties", 'a+') as f:
				f.write(
					str(
						f"\n"
						f"modVersion = 0.1.0\n"
						f"modMinecraftVersion = 1.14.4\n"
						f"modForgeVersion = 28.0.45\n"
						f"mappingsChannel = snapshot\n"
						f"mappingsVersion = {latestMcpSnapshot}\n"
						f"modId = {modID}\n"
						f"modGroup = {userName}.{modName}\n"
						f"modFileName = main\n"
					)
				)
				f.close()
			self.progressBar.setValue((3 / 9) * 100)
			self.errorLab.setText("Running command: \'gradlew eclipse\'")
			self.update()
			time.sleep(0.5)
			os.system("gradlew eclipse")
			self.progressBar.setValue((4 / 9) * 100)
			self.errorLab.setText("Saving Mod Info")
			self.update()
			time.sleep(0.25)
			with open(newDir + "/modInfo.json", "w") as fp:
				emptyList = []
				modInfo = dict()
				modInfo["Name"] = modName
				modInfo["ModId"] = modID
				modInfo["Items"] = emptyList
				modInfo["Blocks"] = emptyList
				modInfo["ToolMats"] = emptyList
				modInfo["ArmorMats"] = emptyList
				InvTabs = [{"Name": "buildingBlocks", "InGameName": "Building Blocks"},
						   {"Name": "decorations", "InGameName": "Decoration Blocks"},
						   {"Name": "redstone", "InGameName": "Redstone"},
						   {"Name": "transportation", "InGameName": "Transportation"},
						   {"Name": "misc", "InGameName": "Miscellaneous"},
						   {"Name": "food", "InGameName": "Foodstuffs"}, {"Name": "tools", "InGameName": "Tools"},
						   {"Name": "combat", "InGameName": "Combat"}, {"Name": "brewing", "InGameName": "Brewing"},
						   {"Name": "materials", "InGameName": "Materials"}]
				modInfo["InvTabs"] = InvTabs
				json.dump(modInfo, fp, indent=4)
				fp.close()
			self.progressBar.setValue((5 / 9) * 100)
			self.errorLab.setText("Removing Example Mod")
			self.update()
			time.sleep(0.5)
			comDir = newDir + "/src/main/java/com"
			shutil.rmtree(comDir)
			self.progressBar.setValue((6 / 9) * 100)
			self.errorLab.setText("Adding Java Path")
			self.update()
			time.sleep(0.5)
			mainDir = newDir + "/src/main/java/" + userName + "/" + modName
			os.makedirs(mainDir)
			#shutil.copyfile("Templates/main.java", mainDir)
			self.progressBar.setValue((7 / 9) * 100)
			self.errorLab.setText("Adding Resource Path")
			self.update()
			time.sleep(0.5)
			assetDir = newDir + "/src/main/resources/assets/" + modID
			os.makedirs(assetDir)
			blockstatesDir = assetDir + "/blockstates"
			os.makedirs(blockstatesDir)
			langDir = assetDir + "/lang"
			os.makedirs(langDir)
			modelsDir = assetDir + "/models"
			os.makedirs(modelsDir)
			modelsBlockDir = modelsDir + "/block"
			os.makedirs(modelsBlockDir)
			modelsItemDir = modelsDir + "/item"
			os.makedirs(modelsItemDir)
			texturesDir = assetDir + "/textures"
			os.makedirs(texturesDir)
			texturesBlockDir = texturesDir + "/block"
			os.makedirs(texturesBlockDir)
			texturesItemDir = texturesDir + "/items"
			os.makedirs(texturesItemDir)
			texturesEntitiesDir = texturesDir + "/entities"
			os.makedirs(texturesEntitiesDir)
			textureArmorModelsDir = texturesDir + "/models/armor"
			os.makedirs(textureArmorModelsDir)
			dataDir = newDir + "/src/main/resources/data/" + modID
			os.makedirs(dataDir)
			recipesDir = dataDir + "/recipes"
			os.makedirs(recipesDir)
			lootTablesDir = dataDir + "/loot_tables"
			os.makedirs(lootTablesDir)
			lootTablesBlocksDir = lootTablesDir + "/blocks"
			os.makedirs(lootTablesBlocksDir)
			lootTablesEntitiesDir = lootTablesDir + "/entities"
			os.makedirs(lootTablesEntitiesDir)
			itemTagsDir = dataDir + "/tags/items"
			os.makedirs(itemTagsDir)
			self.progressBar.setValue((8 / 9) * 100)
			self.update()
			time.sleep(0.5)
			os.chdir(langDir)
			with open("en_us.json", 'x') as fp:
				fp.seek(0)
				json.dump({}, fp, indent=4)
				fp.truncate()
				fp.close()
			self.progressBar.setValue((9 / 9) * 100)
			self.errorLab.setText("All Done!")
			self.update()
			time.sleep(1)
		#"""
		except Exception as e:
			self.errorLab.setText("Error: " + str(e))
			self.update()
			return False
		#"""
		else:
		#if True:
			self.errorLab.setText("Mod Creation Successful...Opening Easy-Editor")
			self.update()
			time.sleep(1)
			self.easy_editor_window.show()
			return True


class EasyEditor(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()
		self.easy_editor_window = self

	def init_ui(self):
		self.TitleLab = QtWidgets.QLabel('Edit An MC 1.14.4 Mod')
		self.modDirLab = QtWidgets.QLabel("Mod Directory:")
		self.modDirPicker = QtWidgets.QComboBox(self)
		self.modDirPicker.addItem("Select Directory")
		self.funcPickerLab = QtWidgets.QLabel("Function:")
		self.funcPicker = QtWidgets.QComboBox(self)
		self.loadFuncs()
		self.submitButton = QtWidgets.QPushButton("Edit Mod")
		self.errorLab = QtWidgets.QLabel('')

		self.main_v_box = self.editorLayout()
		self.setLayout(self.main_v_box)

		self.modDirPicker.activated[str].connect(self.pickNewDirectory)
		self.submitButton.clicked.connect(self.runFunc)

		self.setWindowTitle('MC Mod Maker')

	def editorLayout(self):
		titleHbox = QtWidgets.QHBoxLayout()
		titleHbox.addStretch()
		titleHbox.addWidget(self.TitleLab)
		titleHbox.addStretch()

		modDirHbox = QtWidgets.QHBoxLayout()
		modDirHbox.addStretch()
		modDirHbox.addWidget(self.modDirLab)
		modDirHbox.addWidget(self.modDirPicker)
		modDirHbox.addStretch()

		funcPickerHbox = QtWidgets.QHBoxLayout()
		funcPickerHbox.addStretch()
		funcPickerHbox.addWidget(self.funcPickerLab)
		funcPickerHbox.addWidget(self.funcPicker)
		funcPickerHbox.addStretch()

		submitBtnHbox = QtWidgets.QHBoxLayout()
		submitBtnHbox.addStretch()
		submitBtnHbox.addWidget(self.submitButton)
		submitBtnHbox.addStretch()

		errorLabHbox = QtWidgets.QHBoxLayout()
		errorLabHbox.addStretch()
		errorLabHbox.addWidget(self.errorLab)
		errorLabHbox.addStretch()

		v_box = QtWidgets.QVBoxLayout()
		v_box.addStretch()
		v_box.addLayout(titleHbox)
		v_box.addStretch()
		v_box.addLayout(modDirHbox)
		v_box.addLayout(funcPickerHbox)
		v_box.addLayout(submitBtnHbox)
		v_box.addLayout(errorLabHbox)
		v_box.addStretch()

		return v_box

	def pickNewDirectory(self, text):
		if text == "Select Directory":
			self.modDirPicker.clear()
			self.modDir = QtWidgets.QFileDialog.getExistingDirectory()
			self.modDirPicker.addItem(self.modDir)
			self.modDirPicker.addItem("Select Directory")
			self.refreshModInfo()

	def refreshModInfo(self):
		with open(self.modDir + "/modInfo.json", "r") as fp:
			self.modInfo = json.load(fp)
			fp.close()

	def pickTexture(self, text):
		if text == "Select Directory":
			self.itemTextureDirPicker.clear()
			self.itemTextureDir, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter="PNG IMAGE(*.png)")
			self.itemTextureDirPicker.addItem(self.modDir)
			self.itemTextureDirPicker.addItem("Select Directory")

	def loadFuncs(self):
		self.funcPicker.addItem("Select an option")
		with open("funcList.json", "r") as fp:
			funcList = json.load(fp)
			for func in funcList["funcs"]:
				if func["state"] != "Un-Implemented":
					self.funcPicker.addItem(func["name"])
			fp.close()

	def runFunc(self):
		chosenFunc = self.funcPicker.currentText()
		with open("funcList.json", "r") as fp:
			funcList = json.load(fp)
			for func in funcList["funcs"]:
				if chosenFunc == func["name"]:
					#try:
					if True:
						funcToRun = str(func["id"])
						exec(funcToRun)
					#except Exception as e:
						#print(e)
						#self.errorLab.setText(f"Error: {e}")
						#self.show()

	def runExec(self, string):
		exec(string)

	def loadInvTabPicker(self):
		invTabPicker = QtWidgets.QComboBox()
		for tab in self.modInfo["InvTabs"]:
			invTabPicker.addItem(tab["InGameName"])
		invTabPicker.setCurrentIndex(4)
		return invTabPicker

	def getInvTabFromPicker(self, pickerText):
		tabName = "no such tab"
		for tab in self.modInfo["InvTabs"]:
			if pickerText == tab["InGameName"]:
				tabName = tab["Name"]
		return tabName

	"""
	def addBasicItem(self):
		midTitle = QtWidgets.QLabel('Add A Basic Item:')
		itemNameLab = QtWidgets.QLabel('Item Name:')
		itemNameLe = QtWidgets.QLineEdit(self)
		itemInvTabLab = QtWidgets.QLabel('Inventory Tab:')
		itemInvTabPicker = self.loadInvTabPicker()
		itemInGameNameLab = QtWidgets.QLabel('Item In Game Name:')
		itemInGameNameLe = QtWidgets.QLineEdit(self)
		itemTextureLab = QtWidgets.QLabel('Select Texture:')
		self.itemTextureDirPicker = QtWidgets.QComboBox(self)
		self.itemTextureDirPicker.addItem("Select Directory")
		self.itemSubmitButton = QtWidgets.QPushButton("Add Item")
		self.itemCloseButton = QtWidgets.QPushButton("Close Item Adder")

		addBasicItemLayout = self.main_v_box

		midTitleHbox = QtWidgets.QHBoxLayout()
		midTitleHbox.addStretch()
		midTitleHbox.addWidget(midTitle)
		midTitleHbox.addStretch()

		itemNameHbox = QtWidgets.QHBoxLayout()
		itemNameHbox.addStretch()
		itemNameHbox.addWidget(itemNameLab)
		itemNameHbox.addWidget(itemNameLe)
		itemNameHbox.addStretch()

		invTabPickerHbox = QtWidgets.QHBoxLayout()
		invTabPickerHbox.addStretch()
		invTabPickerHbox.addWidget(itemInvTabLab)
		invTabPickerHbox.addWidget(itemInvTabPicker)
		invTabPickerHbox.addStretch()

		gameNameHbox = QtWidgets.QHBoxLayout()
		gameNameHbox.addStretch()
		gameNameHbox.addWidget(itemInGameNameLab)
		gameNameHbox.addWidget(itemInGameNameLe)
		gameNameHbox.addStretch()

		itemTextureHbox = QtWidgets.QHBoxLayout()
		itemTextureHbox.addStretch()
		itemTextureHbox.addWidget(itemTextureLab)
		itemTextureHbox.addWidget(self.itemTextureDirPicker)
		itemTextureHbox.addStretch()

		submitBtnHbox = QtWidgets.QHBoxLayout()
		submitBtnHbox.addStretch()
		submitBtnHbox.addWidget(self.itemCloseButton)
		submitBtnHbox.addStretch()
		submitBtnHbox.addWidget(self.itemSubmitButton)
		submitBtnHbox.addStretch()

		v_box = QtWidgets.QVBoxLayout()
		v_box.addStretch()
		v_box.addLayout(midTitleHbox)
		v_box.addStretch()
		v_box.addLayout(itemNameHbox)
		v_box.addLayout(invTabPickerHbox)
		v_box.addLayout(gameNameHbox)
		v_box.addLayout(itemTextureHbox)
		v_box.addLayout(submitBtnHbox)
		v_box.addStretch()

		addBasicItemLayout.addLayout(v_box)
		self.setLayout(addBasicItemLayout)
		self.update()

		self.runAddItem = False
		self.closeAddItem = False

		self.itemTextureDirPicker.activated[str].connect(self.pickTexture)
		#self.itemSubmitButton.clicked.connect(self.runExec('self.runAddItem = True'))
		#self.itemCloseButton.clicked.connect(self.runExec('self.closeAddItem = True'))
		self.itemSubmitButton.clicked.connect(
			lambda: exec('runAddItem = True', {}, {"runAddItem": self.runAddItem, "True": True}))
		self.itemCloseButton.clicked.connect(
			lambda: exec('closeAddItem = True', {}, {"closeAddItem": self.closeAddItem, "True": True}))
		self.itemSubmitButton.clicked.connect(lambda: (self.runAddItem = True))

		if self.runAddItem:
			print("running runAddItem")
			item = dict()
			item["Name"] = itemNameLe.text()
			item["InvTab"] = self.getInvTabFromPicker(itemInvTabPicker.currentText())
			item["InGameName"] = itemInGameNameLe.text()
			item["TexturePath"] = self.itemTextureDir

			with open(self.modDir + "/modInfo.json", 'r+') as fp:
				data = json.load(fp)
				data["Items"].append(item)
				fp.seek(0)
				json.dump(data, fp, indent=4)
				fp.truncate()
				fp.close()
				self.modInfo = data

			#Add mod java editing here

			#shutil.copyfile(itemTextureDir, self.modDir + '/src/main/resources/assets/' + self.modInfo["ModId"] + '/textures/items', )
			source = self.itemTextureDir
			target = self.modDir + '/src/main/resources/assets/' + self.modInfo["ModId"] + '/textures/items'

			assert not os.path.isabs(source)
			target = os.path.join(target, os.path.dirname(source))

			# create the folders if not already exists
			os.makedirs(target)

			# adding exception handling
			try:
				shutil.copy(source, target)
			except IOError as e:
				print("Unable to copy file. %s" % e)
			except:
				print("Unexpected error:", sys.exc_info())

			print("Item Added!")
			self.runAddItem = False

		if self.closeAddItem:
			print("closing")
			self.setLayout(self.main_v_box)
			self.show()
			keepOpen = False """

	def addBasicItem(self):
		addItemWindow = AddBasicItem()
		addItemWindow.passModInfo(self.modInfo, self.modDir)
		addItemWindow.show()
		print("Item Adder got info and shown")

	def addBasicBlock(self):
		midTitle = QtWidgets.QLabel('Add A Basic Block:')
		blockNameLab = QtWidgets.QLabel('Block Name:')
		blockNameLe = QtWidgets.QLineEdit(self)
		blockInvTabLab = QtWidgets.QLabel('Inventory Tab:')
		blockInvTabPicker = self.loadInvTabPicker()
		blockInGameNameLab = QtWidgets.QLabel('Block In Game Name:')
		blockInGameNameLe = QtWidgets.QLineEdit(self)
		blockSubmitButton = QtWidgets.QPushButton("Add Block")
		blockCloseButton = QtWidgets.QPushButton("Close Block Adder")

		addBasicBlockLayout = self.main_v_box

		midTitleHbox = QtWidgets.QHBoxLayout()
		midTitleHbox.addStretch()
		midTitleHbox.addWidget(midTitle)
		midTitleHbox.addStretch()

		blockNameHbox = QtWidgets.QHBoxLayout()
		blockNameHbox.addStretch()
		blockNameHbox.addWidget(blockNameLab)
		blockNameHbox.addWidget(blockNameLe)
		blockNameHbox.addStretch()

		invTabPickerHbox = QtWidgets.QHBoxLayout()
		invTabPickerHbox.addStretch()
		invTabPickerHbox.addWidget(blockInvTabLab)
		invTabPickerHbox.addWidget(blockInvTabPicker)
		invTabPickerHbox.addStretch()

		gameNameHbox = QtWidgets.QHBoxLayout()
		gameNameHbox.addStretch()
		gameNameHbox.addWidget(blockInGameNameLab)
		gameNameHbox.addWidget(blockInGameNameLe)
		gameNameHbox.addStretch()

		submitBtnHbox = QtWidgets.QHBoxLayout()
		submitBtnHbox.addStretch()
		submitBtnHbox.addWidget(blockCloseButton)
		submitBtnHbox.addStretch()
		submitBtnHbox.addWidget(blockSubmitButton)
		submitBtnHbox.addStretch()

		v_box = QtWidgets.QVBoxLayout()
		v_box.addStretch()
		v_box.addLayout(midTitleHbox)
		v_box.addStretch()
		v_box.addLayout(blockNameHbox)
		v_box.addLayout(invTabPickerHbox)
		v_box.addLayout(gameNameHbox)
		v_box.addLayout(submitBtnHbox)
		v_box.addStretch()

		addBasicBlockLayout.addLayout(v_box)
		self.setLayout(addBasicBlockLayout)
		self.update()

		runAddBlock = False
		closeAddBlock = False

		blockSubmitButton.clicked.connect(
			lambda: exec('runAddBlock = True', {}, {"runAddBlock": runAddBlock, "True": True}))
		blockCloseButton.clicked.connect(
			lambda: exec('closeAddBlock = True', {}, {"closeAddBlock": closeAddBlock, "True": True}))

		if runAddBlock:
			print("running runAddBlock")
			block = dict()
			block["Name"] = blockNameLe.text()
			block["InvTab"] = self.getInvTabFromPicker(blockInvTabPicker.currentText())
			block["InGameName"] = blockInGameNameLe.text()

			with open(self.modDir + "/modInfo.json", 'r+') as fp:
				data = json.load(fp)
				data["Blocks"].append(block)
				fp.seek(0)
				json.dump(data, fp, indent=4)
				fp.truncate()
				fp.close()
			# Add mod editing here
			print("Block Added!")
			runAddBlock = False

		if closeAddBlock:
			print("closing")
			self.setLayout(self.main_v_box)
			self.show()
			keepOpen = False
		print("bye")

	def addToolMat(self):
		foo = "bar"
		# TO-DO

	def addOreBlock(self):
		foo = "bar"
		# TO-DO

	def addBasicTool(self):
		foo = "bar"
		# TO-DO

	def addBasicToolSet(self):
		foo = "bar"
		# TO-DO

	def addArmorMat(self):
		foo = "bar"
		# TO-DO

	def addArmorSet(self):
		foo = "bar"
		# TO-DO

	def addInvTab(self):
		foo = "bar"
		# TODO : addInvTabb

	def addEntity(self):
		foo = "bar"
		# TO-DO

	def addBiome(self):
		foo = "bar"
		# TO-DO


class AddBasicItem(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.modInfo = {
			"Name": "",
			"ModId": "",
			"Items": [],
			"Blocks": [],
			"ToolMats": [],
			"ArmorMats": [],
			"InvTabs": []
		}
		self.modDir = ""
		print("Item Adder Opened")
		self.init_ui()

	def init_ui(self):
		self.midTitle = QtWidgets.QLabel('Add A Basic Item:')

		self.itemNameLab = QtWidgets.QLabel('Item Name:')
		self.itemNameLe = QtWidgets.QLineEdit(self)

		self.itemInvTabLab = QtWidgets.QLabel('Inventory Tab:')
		self.itemInvTabPicker = self.loadInvTabPicker()

		self.itemInGameNameLab = QtWidgets.QLabel('Item In Game Name:')
		self.itemInGameNameLe = QtWidgets.QLineEdit(self)

		self.itemTypeTab = QtWidgets.QWidget()
		self.itemSpecificTextureTab = QtWidgets.QWidget()
		self.textureTabs = QtWidgets.QTabWidget()
		self.textureTabs.addTab(self.itemTypeTab, "Auto-Generated Texture")
		self.textureTabs.addTab(self.itemSpecificTextureTab, "Saved Texture")

		self.itemTypeLab = QtWidgets.QLabel('Select Item Type:')
		self.itemTypePicker = QtWidgets.QComboBox(self)
		self.itemTypePicker.addItem("Select A Type")

		self.itemTextureLab = QtWidgets.QLabel('Select Texture:')
		self.itemTextureDirPicker = QtWidgets.QComboBox(self)
		self.itemTextureDirPicker.addItem("Select Directory")

		self.itemSubmitButton = QtWidgets.QPushButton("Add Item")
		self.itemCloseButton = QtWidgets.QPushButton("Close Item Adder")

		self.main_v_box = self.addBasicItemLayout()
		self.setLayout(self.main_v_box)

		self.itemTextureDirPicker.activated[str].connect(self.pickTexture)
		self.itemSubmitButton.clicked.connect(self.runAddItem)
		self.itemCloseButton.clicked.connect(self.runClose)

		self.setWindowTitle('MC Mod Maker')
		print("Item Adder UI Loaded")

	def addBasicItemLayout(self):
		midTitleHbox = QtWidgets.QHBoxLayout()
		midTitleHbox.addStretch()
		midTitleHbox.addWidget(self.midTitle)
		midTitleHbox.addStretch()

		itemNameHbox = QtWidgets.QHBoxLayout()
		itemNameHbox.addStretch()
		itemNameHbox.addWidget(self.itemNameLab)
		itemNameHbox.addWidget(self.itemNameLe)
		itemNameHbox.addStretch()

		invTabPickerHbox = QtWidgets.QHBoxLayout()
		invTabPickerHbox.addStretch()
		invTabPickerHbox.addWidget(self.itemInvTabLab)
		invTabPickerHbox.addWidget(self.itemInvTabPicker)
		invTabPickerHbox.addStretch()

		gameNameHbox = QtWidgets.QHBoxLayout()
		gameNameHbox.addStretch()
		gameNameHbox.addWidget(self.itemInGameNameLab)
		gameNameHbox.addWidget(self.itemInGameNameLe)
		gameNameHbox.addStretch()

		textureTabsHbox = QtWidgets.QHBoxLayout()
		textureTabsHbox.addStretch()
		textureTabsHbox.addWidget(self.textureTabs)
		textureTabsHbox.addStretch()

		itemTextureHbox = QtWidgets.QHBoxLayout()
		itemTextureHbox.addStretch()
		itemTextureHbox.addWidget(self.itemTextureLab)
		itemTextureHbox.addWidget(self.itemTextureDirPicker)
		itemTextureHbox.addStretch()
		self.itemSpecificTextureTab.setLayout(itemTextureHbox)

		submitBtnHbox = QtWidgets.QHBoxLayout()
		submitBtnHbox.addStretch()
		submitBtnHbox.addWidget(self.itemCloseButton)
		submitBtnHbox.addStretch()
		submitBtnHbox.addWidget(self.itemSubmitButton)
		submitBtnHbox.addStretch()

		v_box = QtWidgets.QVBoxLayout()
		v_box.addStretch()
		v_box.addLayout(midTitleHbox)
		v_box.addStretch()
		v_box.addLayout(itemNameHbox)
		v_box.addLayout(invTabPickerHbox)
		v_box.addLayout(gameNameHbox)
		v_box.addLayout(textureTabsHbox)
		v_box.addLayout(submitBtnHbox)
		v_box.addStretch()

		print("Item Adder Layout Made")

		return v_box

	def passModInfo(self, modInfoIn, modDirIn):
		self.modInfo = modInfoIn
		self.modDir = modDirIn
		print("Mod info received by Item Adder")

	def loadInvTabPicker(self):
		invTabPicker = QtWidgets.QComboBox()
		for tab in self.modInfo["InvTabs"]:
			invTabPicker.addItem(tab["InGameName"])
		invTabPicker.setCurrentIndex(4)
		print("Inv Tab Picker Loaded for Item Adder")
		return invTabPicker

	def getInvTabFromPicker(self, pickerText):
		tabName = "no such tab"
		for tab in self.modInfo["InvTabs"]:
			if pickerText == tab["InGameName"]:
				tabName = tab["Name"]
		print("Inv Tab received from picker for Item Adder")
		return tabName

	def pickTexture(self, text):
		if text == "Select Directory":
			self.itemTextureDirPicker.clear()
			self.itemTextureDir, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter="PNG IMAGE(*.png)")
			self.itemTextureDirPicker.addItem(self.modDir)
			self.itemTextureDirPicker.addItem("Select Directory")

	def runAddItem(self):
			print("running runAddItem")
			item = dict()
			item["Name"] = self.itemNameLe.text()
			item["InvTab"] = self.getInvTabFromPicker(self.itemInvTabPicker.currentText())
			item["InGameName"] = self.itemInGameNameLe.text()
			item["TexturePath"] = self.itemTextureDir

			with open(self.modDir + "/modInfo.json", 'r+') as fp:
				data = json.load(fp)
				data["Items"].append(item)
				fp.seek(0)
				json.dump(data, fp, indent=4)
				fp.truncate()
				fp.close()
				self.modInfo = data

			#Add mod java editing here

			#shutil.copyfile(itemTextureDir, self.modDir + '/src/main/resources/assets/' + self.modInfo["ModId"] + '/textures/items', )
			source = self.itemTextureDir
			target = self.modDir + '/src/main/resources/assets/' + self.modInfo["ModId"] + '/textures/items'

			assert not os.path.isabs(source)
			target = os.path.join(target, os.path.dirname(source))

			# create the folders if not already exists
			os.makedirs(target)

			# adding exception handling
			try:
				shutil.copy(source, target)
			except IOError as e:
				print("Unable to copy file. %s" % e)
			except:
				print("Unexpected error:", sys.exc_info())

			print("Item Added!")

	def runClose(self):
		print("closing")
		with open(self.modDir + "/modInfo.json", 'r+') as fp:
			data = self.modInfo
			fp.seek(0)
			json.dump(data, fp, indent=4)
			fp.truncate()
			fp.close()
		EasyEditor.easy_editor_window.refreshModInfo()
		self.close()


with open('PyQt5StyleSheet.css', 'r') as styleSheet:
	qss = styleSheet.read()
	app.setStyleSheet(qss)
a_window = HomePage()
sys.exit(app.exec_())
