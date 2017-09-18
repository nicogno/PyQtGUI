from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, os


class Button(QPushButton):

    def __init__(self, title, parent):
        self.p = parent  
        super().__init__(title, parent)
    

    def mouseMoveEvent(self, e):    #(re-implementation of the class-original method)

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())    #Moves the cursor

        dropAction = drag.exec_(Qt.MoveAction)


    def mousePressEvent(self, e):   #(re-implementation of the class-original method)
      
        QPushButton.mousePressEvent(self, e)    #mousePressEvent is also called on the parent window (notice the e argument)
        
        if e.button() == Qt.LeftButton:
            self.p.openFileNameDialog()


class Window(QWidget):
  
    def __init__(self):
        super().__init__()

        self.initUI()
        
        
    def initUI(self):

        self.setAcceptDrops(True)

        button = Button("Open File", self)  #Button settings (self stands for the parent, the window in this case)
        button.move(90,60)

        label = QLabel(self)    #Label settings
        label.setText("Drag and drop a file here or open file")
        label.move(30,40)

        self.setWindowTitle('Data Analyzer')
        self.setGeometry(300, 300, 600, 300)    #(x,y,width,heigth)
        qtRectangle = self.frameGeometry()      #Next 4 lines center the window
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        

    def dragEnterEvent(self, event):    #Check if the event really gave a file path (re-implementation of the class-original method)
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
        

    def dropEvent(self, event): #Called when files are released on the window (re-implementation of the class-original method)
            for url in event.mimeData().urls(): #We already checked the data-type so we can't get errors here
                path = url.toLocalFile()
            if os.path.isfile(path):    #Check wheter the relesed object is a file
                print('File path: '+path)
                #self.close
                #sys.exit()

    def openFileNameDialog(self):    #Called when files are searched from the window
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose the file you want to analyze", "","All Files (*);;Excel Files (*.xlsx);;CSV Files (*.csv)", options=options)
        if fileName:
            print('File path: '+fileName)
            self.close
            sys.exit()
            
  

if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_() 


