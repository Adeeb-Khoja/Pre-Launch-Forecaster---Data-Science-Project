import csv
import os

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot, QPropertyAnimation, QCoreApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMainWindow
from mainwindow import Ui_MainWindow
from window2 import Ui_ViewGraphs
from upload import Model
from models import Models
from PDF import PDF
from featuresPrediction import Feature
import sys
import matplotlib.pyplot as plt

import time


class MainWindowUIClass(Ui_MainWindow):

    def __init__(self):
        """
        Initialize the super class
        """
        super().__init__()
        self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        self.upload = Model()
        self.models = Models()
        self.features = Feature()
        self.widnow2 = Ui_ViewGraphs()
        self.pdfclass = PDF()
        # models
        self.dataseNAme = " "
        self.price = " "
        self.cluster = " "
        self.satis = " "
        self.feature = []
        self.predictedScore = []
        self.accuracy = []
        self.volume = " "
        self.image1 = " "
        self.image2 = " "

    def setupUi(self, MW):
        """ Setup the UI of the super class, and add here code
        that relates to the way we want our UI to operate.
        """
        super().setupUi(MW)
        # --------------------------------------Main buttons--------------------------------------------#
        self.btn_check.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.check_page))
        self.btn_upload.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.upload_page))
        self.btn_update.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.update_page))
        self.btn_issue.clicked.connect(lambda: self.reportPage())
        # --------------------------------------upload page buttons-------------------------------------#
        self.pushButton.clicked.connect(lambda: self.browseSlot())
        self.pushButton_2.clicked.connect(lambda: self.writeDocSlot())
        self.lineEdit.returnPressed.connect(lambda: self.returnPressedSlot())
        self.btn_upload_2.clicked.connect(lambda: self.cloud_upload(self.upload.getFileName()))
        # --------------------------------------Update page buttons-------------------------------------#
        self.pushButton_5.clicked.connect(lambda: self.browse())
        self.pushButton_3.clicked.connect(lambda: self.save_sheet())
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(35)
        self.table()

        # --------------------------------------Find page buttons-------------------------------------#
        self.btn_findDataset.clicked.connect(lambda: self.find_datasets())
        # --------------------------------------Issue Report------------------------------------------#
        self.comboBOX()
        self.disableButton()
        self.btn_downloadReport.clicked.connect(lambda: self.pdf())
        self.btn_issue_read.clicked.connect(lambda: self.read_Predictions())
        self.btn_issue_view.clicked.connect(lambda: self.graphs())
        self.btn_predictScore.clicked.connect(lambda: self.btn_features())
        self.btn_predicSales.clicked.connect(lambda: self.btn_PedictSales())

        #
        self.btn_list.clicked.connect(lambda: self.toggleMenu(160, True))

    def pdf(self):
        returnedPDF = self.pdfclass.dataset(self.dataseNAme)
        #Price
        # returnedPDF.cell(20, 10, 'The Predicted Price is: ' + str(self.price) + "$", 0, 1)
        returnedPDF.print_chapter(2, 'Predicted Price', 'price.txt', str(self.price)+"$")
        returnedPDF.print_chapter(3, 'Classification Cluster', 'cluster.txt',  str(self.cluster))
        returnedPDF.print_chapter(4, 'Customer Satisfaction ', 'statisfacation.txt', str(self.satis))
        returnedPDF.print_chapter(5, 'Features ', 'empty.txt', ':')
        returnedPDF.cell(10, 10, '', 0, 1)

        returnedPDF.cell(10, 10, 'Features: ' + str(self.feature), 0, 1)

        returnedPDF.cell(10, 10, 'Predicted Score for each feature is: ' + str(self.predictedScore), 0, 1)

        returnedPDF.cell(10, 10, 'Accuracy for feature is: ' + str(self.accuracy), 0, 1)

        returnedPDF.print_chapter(6, 'Graphs ', 'graphs.txt', ' ')

        returnedPDF.image(os.path.basename(self.image1), 10, 100, 90, 90)
        returnedPDF.image(os.path.basename(self.image2), 10, 180, 90, 90)

        returnedPDF.output('rep1.pdf', 'F')

    def graphs(self):
        self.widnow = QtWidgets.QMainWindow()
        self.ui = Ui_ViewGraphs()
        self.ui.setupUi(self.widnow)
        try:
            names = self.upload.getFrom_cloud()
            file_name = self.comboBox.currentText().replace("Datasets/", "").replace(".csv", "")
            matching = [s for s in names if "Graphs/" + file_name in s]
            print(matching[0])
            self.image = QImage()
            self.imageURL = self.upload.returnURL(matching[0].replace("%20", " "))

            self.image.loadFromData(requests.get(self.imageURL).content)
            print(self.imageURL)
            self.image1 = self.upload.downloadGraph(matching[0].replace("%20", " "))
            self.ui.pic1.setPixmap(QPixmap(self.image.scaled(700, 700)))
            self.ui.pic1.setMaximumSize(QtCore.QSize(800, 1000))
            self.ui.pic1.setScaledContents(True)
            self.ui.pic1.show()
            #
            self.imageURL = self.upload.returnURL(matching[1].replace("%20", " "))
            self.image.loadFromData(requests.get(self.imageURL).content)
            print(self.imageURL)
            self.image2 = self.upload.downloadGraph(matching[1].replace("%20", " "))
            self.ui.pic2.setPixmap(QPixmap(self.image.scaled(700, 700)))
            self.ui.pic2.setMaximumSize(QtCore.QSize(800, 1000))
            self.ui.pic2.setScaledContents(True)
            self.ui.pic2.show()
        except:
            print("images dont exist")

        # self.ui.pic2.setText(image1)
        self.widnow.show()

    def comboBOX(self):
        names = self.upload.getFrom_cloud()
        if not names:
            print("Database is empty")
        else:
            self.comboBox.clear()
            for x in range(len(names)):
                if "csv" in names[x]:
                    self.comboBox.addItem(names[x])
        self.dataseNAme = self.comboBox.currentText()

    def reportPage(self):
        self.comboBOX()
        self.stackedWidget.setCurrentWidget(self.issue_opage)

    def btn_features(self):
        print(self.txt_feature.text())
        if not self.txt_feature.text():
            self.txt_predictions.append("Fill text field")
        else:
            try:
                self.features.pred(str(self.txt_feature.text()))
                self.txt_predictions.append(
                    "Predicted score(" + self.txt_feature.text() + "): " + str(self.features.predicted_score))
                self.feature.append(str(self.txt_feature.text()))
                self.predictedScore.append(str(self.features.predicted_score))
                self.accuracy.append(str(self.features.predicted_accuracy))
            except:
                self.txt_predictions.append("item doesn't exist")

    def btn_PedictSales(self):
        if not self.txt_period.text() or not self.txt_volume.text():
            self.txt_predictions.append("Fill text field")
        else:
            file_name = self.comboBox.currentText().replace("Datasets/", "").replace(".csv", "")

            try:
                self.models.callSalesModel(self.txt_volume.text(), self.txt_period.text(), file_name)

            except:
                print("Difusion Model offline or wrong input format")
        time.sleep(5)

        self.enableButton()

    def toggleMenu(self, maxWidth, enable):
        if enable:
            # GET WIDTH
            width = self.Buttons_Frame.width()
            maxExtend = maxWidth
            standard = 35

            # SET MAX WIDTH
            if width == 35:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.Buttons_Frame, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def plot_graph(self):
        # hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        # pen = pg.mkPen(color=(255, 0, 0))
        # self.graphWidget.plot(hour, temperature, pen=pen)
        file_name = self.comboBox.currentText().replace("Datasets/", "").replace(".csv", "")

        try:
            names = self.upload.getFrom_cloud()
            matching = [s for s in names if "Graphs/" + file_name in s]
            print(matching[0])
            self.image = QImage()
            self.imageURL = self.upload.returnURL(matching[0])
            self.image.loadFromData(requests.get(self.imageURL).content)
            self.lbl_pic_1.setPixmap(QPixmap(self.image.scaled(600, 500)))
            self.lbl_pic_1.setMaximumSize(QtCore.QSize(800, 1000))
            self.lbl_pic_1.setScaledContents(True)
            self.lbl_pic_1.show()

            self.imageURL = self.upload.returnURL(matching[1])
            self.image.loadFromData(requests.get(self.imageURL).content)
            self.lbl_pic_2.setPixmap(QPixmap(self.image.scaled(600, 500)))
            self.lbl_pic_2.setMaximumSize(QtCore.QSize(800, 1000))
            self.lbl_pic_2.setScaledContents(True)
            self.lbl_pic_2.show()
        except:
            print("Images don't exist")

        # Load combobox
        #

    def read_Predictions(self):
        # Download the selected dataset
        datasetName = self.upload.downloadDataset(self.comboBox.currentText())
        self.dataseNAme = datasetName
        self.txt_predictions.setText("")
        # calling the price model
        try:
            price = str(self.models.callPriceModel(datasetName))
            self.txt_predictions.append("Predicted Price:" + price + "$")
            self.price = price
        except:
            self.txt_predictions.append("Price model Offline or wrong dataset format")

        # calling the cluster model
        try:
            cluster = str(self.models.callClasificationModel(datasetName))
            self.txt_predictions.append(
                'Classificattion Cluster: ' + cluster)
            self.cluster = cluster
        except:
            self.txt_predictions.append("Cluster model Offline or wrong dataset format")

        # calling satisfaction model
        try:
            satis = str(self.models.callStatisfactionModel(datasetName))
            self.txt_predictions.append('Customer Stisfaction: ' + satis)
            self.satis = satis
        except:
            self.txt_predictions.append("Stisfaction model Offline or wrong dataset format")

    def find_datasets(self):
        self.textBrowser_2.setText("")
        names = self.upload.getFrom_cloud()
        if not names:
            self.textBrowser_2.append("Database is empty")
        else:
            for x in range(len(names)):
                self.textBrowser_2.append(str(names[x]))

    def cloud_upload(self, filename):
        if self.upload.isValid(filename):
            self.upload.upload_cloud(filename.rsplit('/', 1)[1])
            msg = filename.rsplit('/', 1)[1] + " uploaded successfully"
            self.debugPrint(msg)
        else:
            msg = "File not valid " + filename
            self.debugPrint(msg)

    def browse(self):
        self.CSV()

    def CSV(self):
        path = QFileDialog.getOpenFileName(QFileDialog(), "Open CSV", os.getenv('HOME'), "csv(*.csv)")
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(10)
                my_file = csv.reader(csv_file, dialect='excel')
                for row_data in my_file:
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    if len(row_data) > 10:
                        self.tableWidget.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.tableWidget.setItem(row, column, item)
        self.lineEdit_5.setText(path[0])

    def save_sheet(self):
        path = QFileDialog.getSaveFileName(QFileDialog(), 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.tableWidget.rowCount()):
                    row_data = []
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)

    def debugPrint(self, msg):
        """Print the message in the text edit at the bottom of the
        horizontal splitter.
        """
        self.textBrowser.append(msg)

    def refreshAll(self):
        """
        Updates the widgets whenever an interaction happens.
        Typically some interaction takes place, the UI responds,
        and informs the model of the change.  Then this method
        is called, pulling from the model information that is
        updated in the GUI.
        """
        self.lineEdit.setText(self.upload.getFileName())
        self.textEdit.setText(self.upload.getFileContents())

    # slot
    def returnPressedSlot(self):
        """ Called when the user enters a string in the line edit and
        presses the ENTER key.
        """
        fileName = self.lineEdit.text()
        if self.upload.isValid(fileName):
            self.upload.setFileName(self.lineEdit.text())
            self.refreshAll()
        else:
            m = QtWidgets.QMessageBox()
            m.setText("Invalid file name!\n" + fileName)
            m.setIcon(QtWidgets.QMessageBox.Warning)
            m.setStandardButtons(QtWidgets.QMessageBox.Ok
                                 | QtWidgets.QMessageBox.Cancel)
            m.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = m.exec_()
            self.lineEdit.setText("")
            self.refreshAll()
            self.debugPrint("Invalid file specified: " + fileName)

    # slot
    def writeDocSlot(self):
        """ Called when the user presses the Write-Doc button.
        """
        self.upload.writeDoc(self.textEdit.toPlainText())
        self.debugPrint("Document saved")

    # slot
    def browseSlot(self):
        """ Called when the user presses the Browse button
        """
        # self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(QFileDialog(), "Open CSV", os.getenv('HOME'), "csv(*.csv)")
        if fileName:
            self.debugPrint("setting file name: " + fileName)
            self.upload.setFileName(fileName)
            self.refreshAll()

    def disableButton(self):
        self.btn_issue_view.setEnabled(False)
        self.btn_issue_view.setStyleSheet("QPushButton{\n"
                                          "\n"
                                          "background-color:black;\n"
                                          "color:gray;\n"
                                          "}\n"
                                          "QPushButton:hover {\n"
                                          "background-color: rgb(57, 65, 80);\n"
                                          "    border: 2px solid rgb(61, 70, 86);\n"
                                          "}\n"
                                          "QPushButton:pressed {    \n"
                                          "    background-color: rgb(35, 40, 49);\n"
                                          "}    border: 2px solid rgb(43, 50, 61);")

    def enableButton(self):
        self.btn_issue_view.setEnabled(True)
        self.btn_issue_view.setStyleSheet("QPushButton{\n"
                                          "\n"
                                          "background-color:rgb(52, 59, 72);\n"
                                          "color:white;\n"
                                          "}\n"
                                          "QPushButton:hover {\n"
                                          "background-color: rgb(57, 65, 80);\n"
                                          "    border: 2px solid rgb(61, 70, 86);\n"
                                          "}\n"
                                          "QPushButton:pressed {    \n"
                                          "    background-color: rgb(35, 40, 49);\n"
                                          "}    border: 2px solid rgb(43, 50, 61);")

    def table(self):
        item = QTableWidgetItem('horsepower')
        self.tableWidget.setItem(0, 0, item)
        item = QTableWidgetItem('carwidth')
        self.tableWidget.setItem(0, 1, item)
        item = QTableWidgetItem('carbody')
        self.tableWidget.setItem(0, 2, item)
        item = QTableWidgetItem('enginetype')
        self.tableWidget.setItem(0, 3, item)
        item = QTableWidgetItem('Ratings')
        self.tableWidget.setItem(0, 4, item)
        item = QTableWidgetItem('Model')
        self.tableWidget.setItem(0, 5, item)
        item = QTableWidgetItem('Year')
        self.tableWidget.setItem(0, 6, item)
        item = QTableWidgetItem('Engine_HP')
        self.tableWidget.setItem(0, 7, item)
        item = QTableWidgetItem('Engine_Cylinders')
        self.tableWidget.setItem(0, 8, item)
        item = QTableWidgetItem('Driven_Wheels')
        self.tableWidget.setItem(0, 9, item)
        item = QTableWidgetItem('Number_of_Doors')
        self.tableWidget.setItem(0, 10, item)
        item = QTableWidgetItem('Market_Category')
        self.tableWidget.setItem(0, 11, item)
        item = QTableWidgetItem('Vehicle_Size')
        self.tableWidget.setItem(0, 12, item)
        item = QTableWidgetItem('highway_MPG')
        self.tableWidget.setItem(0, 13, item)
        item = QTableWidgetItem('city_mpg')
        self.tableWidget.setItem(0, 14, item)
        item = QTableWidgetItem('Vehicle_Style')
        self.tableWidget.setItem(0, 15, item)
        item = QTableWidgetItem('Sentiment')
        self.tableWidget.setItem(0, 16, item)
        item = QTableWidgetItem('fueltype')
        self.tableWidget.setItem(0, 17, item)
        item = QTableWidgetItem('aspiration')
        self.tableWidget.setItem(0, 18, item)
        item = QTableWidgetItem('cylindernumber')
        self.tableWidget.setItem(0, 19, item)
        item = QTableWidgetItem('drivewheel')
        self.tableWidget.setItem(0, 20, item)
        item = QTableWidgetItem('wheelbase')
        self.tableWidget.setItem(0, 21, item)
        item = QTableWidgetItem('curbweight')
        self.tableWidget.setItem(0, 22, item)
        item = QTableWidgetItem('enginesize')
        self.tableWidget.setItem(0, 23, item)
        item = QTableWidgetItem('boreratio')
        self.tableWidget.setItem(0, 24, item)
        item = QTableWidgetItem('highwaympg')
        self.tableWidget.setItem(0, 25, item)
        item = QTableWidgetItem('carlength')
        self.tableWidget.setItem(0, 26, item)
        item = QTableWidgetItem('cluster')
        self.tableWidget.setItem(0, 27, item)
        item = QTableWidgetItem('Transimission_type')
        self.tableWidget.setItem(0, 28, item)


def main():
    """
    This is the MAIN ENTRY POINT of our application.  The code at the end
    of the mainwindow.py script will not be executed, since this script is now
    our main program.   We have simply copied the code from mainwindow.py here
    since it was automatically generated by '''pyuic5'''.

    """
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


main()
