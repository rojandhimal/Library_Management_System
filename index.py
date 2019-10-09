from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#import MySQLdb
import mysql.connector


from PyQt5.uic import loadUiType

import sys

ui,_ = loadUiType('library.ui')
class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()

        self.show_category()
        self.show_Author()
        self.show_Publisher()

        self.show_Category_Conbobox()
        self.show_Author_Combobox()
        self.show_Publisher_Combobox()

        
        
    def Handel_UI_Changes(self):
        """Include all changes made in UI of the system """
        self.Hiding_themes()
        self.tabWidget.tabBar().setVisible(False)
  


    def Handel_Buttons(self):
        """All button action are handeled in this method"""
        self.themeButton.clicked.connect(self.Show_themes)  #if Themes button clicked goto Show_themes 
        self.closeThemeBtn.clicked.connect(self.Hiding_themes) #if close theme btn clicked goto hiding_themes

        self.DailyOperBtn.clicked.connect(self.open_Day_To_Dat_operations_tab)  #if DailyOperBtn goto open_Day_to day method
        self.booksBtn.clicked.connect(self.open_Books_tab)
        self.usersBtn.clicked.connect(self.open_User_Tab)
        self.settingsBtn.clicked.connect(self.open_Settings_tab)
        self.addBookBtn.clicked.connect(self.add_New_Book)
        self.addNewCategryBtn.clicked.connect(self.add_category)
        self.addautherBtn.clicked.connect(self.add_Author)  #if addautherBtn clicked then goto add_auther method
        self.addpublisherBtn.clicked.connect(self.add_Publisher)    #if addpublisherBtn clicked then goto add_publisher method
        self.searchBtn.clicked.connect(self.search_Book)
        self.updateBookBtn.clicked.connect(self.edit_Book)
        self.deleteBookBtn.clicked.connect(self.delete_Book)

        self.pushButton_addNewUser.clicked.connect(self.add_New_user)
        self.pushButton_userlogin.clicked.connect(self.login_user)

    def Show_themes(self):
        """This show the theme dialogbox after button pressed"""
        self.groupBox_3.show()
        

    def Hiding_themes(self):
        """This hides the theme dialogbox after button pressed"""
        self.groupBox_3.hide()

    def open_Day_To_Dat_operations_tab(self):
        """This opens day to day task tab """
        self.tabWidget.setCurrentIndex(0)

    def open_Books_tab(self):
        """This opens books tabs """
        self.tabWidget.setCurrentIndex(1)

    def open_User_Tab(self):
        """This opens users tab"""
        self.tabWidget.setCurrentIndex(2)

    def open_Settings_tab(self):
        """This open settings tabs"""
        self.tabWidget.setCurrentIndex(3)

    """Books"""

    def add_New_Book(self):
        """This add book details"""
        self.db = mysql.connector.connect(host='localhost',user='root',passwd="arnakhadi16",database="library")
        self.cur = self.db.cursor()
        book_title = self.LineEditbookTitle.text()
        book_description=self.textEdit_4.toPlainText()
        book_code = self.lineEdit_25.text()
        book_category = self.comboBox_category.currentIndex()
        book_author = self.comboBox_author.currentIndex()
        book_publisher = self.comboBox_publisher.currentIndex()
        book_price = self.lineEdit_price.text()
        self.cur.execute("INSERT INTO book(book_name,book_description,book_code,book_category,book_author,book_publisher,book_price) VALUES (%s, %s, %s, %s, %s, %s, %s)", (book_title,book_description,book_code,book_category,book_author,book_publisher,book_price))
        self.db.commit()
        self.statusBar().showMessage('New Book {} Added'.format(book_title))


        self.LineEditbookTitle.setText('')
        self.textEdit_4.setPlainText('')
        self.lineEdit_25.setText('')
        self.comboBox_category.setCurrentIndex(0)
        self.comboBox_author.setCurrentIndex(0)
        self.comboBox_publisher.setCurrentIndex(0)
        self.lineEdit_price.setText('')

    def search_Book(self):
        book_title = self.lineEdit_search.text()
        self.db_connect()

        sql = "SELECT * FROM book WHERE book_name = %s"
        self.cur.execute(sql, [(book_title)])

        data = self.cur.fetchone()
        print("Search book name ={}" .format(data))
        
        self.lineEdit_booktitle.setText(data[1])
        self.textEdit_editbook.setText(data[2])
        self.lineEdit_bookcode.setText(data[3])
        self.comboBox_category_2.setCurrentIndex(data[4])
        self.comboBox_author.setCurrentIndex(data[5])
        self.comboBox_publisher.setCurrentIndex(data[6])
        self.lineEdit_priceSearch.setText(str(data[7]))
     
     
    def edit_Book(self):
        self.db_connect()
        book_name = self.lineEdit_booktitle.text()
        book_description = self.textEdit_editbook.toPlainText()
        book_code = self.lineEdit_bookcode.text()
        book_category = self.comboBox_category_2.currentIndex()
        book_author = self.comboBox_author.currentIndex()
        book_publisher = self.comboBox_publisher.currentIndex()
        book_price = self.lineEdit_priceSearch.text()

        search_book_title = self.lineEdit_search.text()
        self.cur.execute("UPDATE library.book SET book_name=%s,book_description=%s,book_code=%s,book_category=%s,book_author=%s,book_publisher=%s,book_price=%s WHERE book_name=%s", (book_name, book_description, book_code, book_category,book_author, book_publisher, book_price,search_book_title))
        self.db.commit()
        self.statusBar().showMessage("{} Book Updated".format(book_name))

        self.lineEdit_booktitle.setText("")
        self.textEdit_editbook.setPlainText("")
        self.lineEdit_bookcode.setText("")
        self.comboBox_category_2.setCurrentIndex(0)
        self.comboBox_author.setCurrentIndex(0)
        self.comboBox_publisher.setCurrentIndex(0)
        self.lineEdit_priceSearch.setText("")

        

    def delete_Book(self):
        self.db_connect()

        book_title = self.lineEdit_search.text()
        warning = QMessageBox.warning(self, 'Delete Book',"Are you sure  want to delete this book?", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = "DELETE FROM library.book WHERE book_name=%s"
            self.cur.execute(sql, [(book_title)])
            self.db.commit()
            self.statusBar().showMessage("{} Book deleted".format(book_title))

            self.lineEdit_booktitle.setText("")
            self.textEdit_editbook.setPlainText("")
            self.lineEdit_bookcode.setText("")
            self.comboBox_category_2.setCurrentIndex(0)
            self.comboBox_author.setCurrentIndex(0)
            self.comboBox_publisher.setCurrentIndex(0)
            self.lineEdit_priceSearch.setText("")


    """User"""

    def add_New_user(self):
        username = self.lineEdit_username.text()
        email = self.lineEdit_email.text()
        password1 = self.lineEdit_password1.text()
        password2 = self.lineEdit_password2.text()

        if password1 == password2:
            self.cur.execute("INSERT INTO users(username,email,password) VALUES (%s, %s, %s)", (username,email,password1))
            self.db.commit()
            self.statusBar().showMessage('New user {} Added'.format(username))

            self.lineEdit_username.setText("")
            self.lineEdit_email.setText("")
            self.lineEdit_password1.setText("")
            self.lineEdit_password2.setText("")
            self.label_errormessage.setText("")

        else:
            self.label_errormessage.setText("Please Enter Same Password!")


    def login_user(self):
        self.db_connect()

        username = self.lineEdit_loginUsername.text()
        password = self.lineEdit_loginPassword.text()

        sql = "SELECT username,password,email FROM library.users"

        self.cur.execute(sql)
        data = self.cur.fetchall()

        for row in data:
            if username == row[0] and password == row[1]:
                 self.statusBar().showMessage('Welcome {} '.format(username))
                 self.groupBox_edituser.setEnabled(True)

                 self.lineEdit_editUsername.setText(row[0])
                 self.lineEdit_editEmail.setText(row[2])
                 self.lineEdit_editPassword1.setText(row[1])
                 self.lineEdit_editPassword2.setText('')
            else:
                self.statusBar().showMessage('User not Found!')
                    

    def edit_user(self):
        pass

    """Settings"""
    def add_category(self):
        """Insert category in database"""
        self.db = mysql.connector.connect(host='localhost',user='root',passwd="arnakhadi16",database="library")
        self.cur = self.db.cursor()

        category_name = self.lineEdit_22.text()

        self.cur.execute("INSERT INTO category(category_name) VALUES (%s)", (category_name,))

        self.db.commit()
        self.statusBar().showMessage('New category {} Added'.format(category_name))
        self.show_category()
        self.lineEdit_22.setText('')
        self.show_category()
        self.show_Category_Conbobox()


    def show_category(self):
        """This display all category"""
        self.db = mysql.connector.connect(host='localhost',user='root',passwd="arnakhadi16",database="library")
        self.cur = self.db.cursor()

        self.cur.execute('''Select category_name from category''')

        data = self.cur.fetchall()
        print("Categories : {}".format(data))
        if data:
            self.tableWidget_categories.setRowCount(0)
            self.tableWidget_categories.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_categories.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_categories.rowCount()
                self.tableWidget_categories.insertRow(row_position)


        


    def add_Author(self):
        """Add athor in database"""
        self.db = mysql.connector.connect(host='localhost',user='root',passwd="arnakhadi16",database="library")
        self.cur = self.db.cursor()

        author_name = self.lineEdit_author.text()

        self.cur.execute("INSERT INTO authors(author_name) VALUES (%s)", (author_name,))

        self.db.commit()
        self.statusBar().showMessage('New Author {} Added'.format(author_name))
        self.lineEdit_author.setText('')
        self.show_Author()
        self.show_Author_Combobox()

    def show_Author(self):
        """This show all auther"""
        self.db = mysql.connector.connect(host='localhost',user='root',passwd="arnakhadi16",database="library")
        self.cur = self.db.cursor()

        self.cur.execute('''Select author_name from authors''')

        data = self.cur.fetchall()
        print("Authors : {}".format(data))
        if data:
            self.tableWidget_authors.setRowCount(0)
            self.tableWidget_authors.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_authors.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_authors.rowCount()
                self.tableWidget_authors.insertRow(row_position)



    def add_Publisher(self):
        """This add Publisher in database"""
        self.db = mysql.connector.connect(host='localhost',user='root',passwd="arnakhadi16",database="library")
        self.cur = self.db.cursor()

        publisher_name = self.lineEdit_publish.text()

        self.cur.execute("INSERT INTO publisher(publisher_name) VALUES (%s)", (publisher_name,))

        self.db.commit()
        self.statusBar().showMessage('New Publisher {} Added '.format(publisher_name))
        self.lineEdit_publish.setText('')
        self.show_Publisher()
        self.show_Publisher_Combobox()

    def db_connect(self):
        self.db = mysql.connector.connect(host='localhost',user='root',passwd="arnakhadi16",database="library")
        self.cur = self.db.cursor()

    def show_Publisher(self):
        """This display all publisher"""
        self.db = mysql.connector.connect(host='localhost',user='root',passwd="arnakhadi16",database="library")
        self.cur = self.db.cursor()

        self.cur.execute('''Select publisher_name from publisher''')

        data = self.cur.fetchall()
        print("Publisher : {}".format(data))
        if data:
            self.tableWidget_publishers.setRowCount(0)
            self.tableWidget_publishers.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_publishers.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_publishers.rowCount()
    
                self.tableWidget_publishers.insertRow(row_position)

    #####################################################
    ##############show setting data in category##########
    #####################################################

    def show_Category_Conbobox(self):
        self.db_connect()
        self.cur.execute("Select category_name from category")
        data = self.cur.fetchall()

        self.comboBox_category.clear()
        for category in data:
           # print(category[0])
            self.comboBox_category.addItem(category[0])
            self.comboBox_category_2.addItem(category[0])


    def show_Author_Combobox(self):
        self.db_connect()
        self.cur.execute("Select author_name from authors")
        data = self.cur.fetchall()

        self.comboBox_author.clear()
        for category in data:
           # print(category[0])
            self.comboBox_author.addItem(category[0])
            self.comboBox_author_2.addItem(category[0])


    
    def show_Publisher_Combobox(self):
        self.db_connect()
        self.cur.execute("Select publisher_name from publisher")
        data = self.cur.fetchall()

        self.comboBox_publisher.clear()
        for category in data:
           # print(category[0])
            self.comboBox_publisher.addItem(category[0])
            self.comboBox_publisher_2.addItem(category[0])

    


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()