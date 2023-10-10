from PySide2.QtWidgets import *  # type: ignore
from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from pathlib import Path
import dns.rdatatype
import dns.message   #  --> pip install dnspython
import threading
import requests      #  --> pip install requests
import base64
import socket
import random
import time
import sys
import os


listen_PORT = 4800    # pyprox listening to 127.0.0.1:listen_PORT
#num_fragment = 15  # total number of chunks that ClientHello devided into (chunks with random size)
fragment_sleep = 0.001  # sleep between each fragment to make GFW-cache full so it forget previous chunks. LOL.
log_every_N_sec = 30   # every 30 second , update log file with latest DNS-cache statistics
allow_insecure = True   # set true to allow certificate domain mismatch in DoH


class Ui_MainWindow(object):
    global num_fragment
    global checkbox_status 
    def setupUi(self, MainWindow):
        global log
        Ui_MainWindow.num_fragment = 0
        Ui_MainWindow.checkbox_status = 0
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(631, 491)
        MainWindow.setMinimumSize(QSize(631, 491))
        MainWindow.setMaximumSize(QSize(631, 491))
        MainWindow.setAnimated(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 631, 501))
        self.tabWidget.setStyleSheet(u"")
        self.main = QWidget()
        self.main.setObjectName(u"main")
        self.label_2 = QLabel(self.main)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 10, 111, 16))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.righ_checkbox = QCheckBox(self.main)
        self.righ_checkbox.setObjectName(u"righ_checkbox")
        self.righ_checkbox.setGeometry(QRect(10, 120, 84, 24))
        self.frag_log = QTextBrowser(self.main)
        self.frag_log.setObjectName(u"frag_log")
        self.frag_log.setGeometry(QRect(-10, 220, 641, 161))
        self.mci_checkbox = QCheckBox(self.main)
        self.mci_checkbox.setObjectName(u"mci_checkbox")
        self.mci_checkbox.setEnabled(True)
        self.mci_checkbox.setGeometry(QRect(10, 90, 101, 24))
        log = QTextBrowser(self.main)
        log.setObjectName(u"log")
        log.setGeometry(QRect(170, 0, 471, 231))
        self.icell_checkbox = QCheckBox(self.main)
        self.icell_checkbox.setObjectName(u"icell_checkbox")
        self.icell_checkbox.setGeometry(QRect(10, 60, 84, 24))
        self.icell_checkbox.setChecked(False)
        self.frag_checker = QPushButton(self.main)
        self.frag_checker.setObjectName(u"frag_checker")
        self.frag_checker.setGeometry(QRect(140, 410, 88, 28))
        self.frag_checker.setStyleSheet(u"")
        self.frag_checker.setEnabled(False)
        self.frag_status = QLineEdit(self.main)
        self.frag_status.setObjectName(u"frag_status")
        self.frag_status.setGeometry(QRect(20, 30, 113, 28))
        self.textBrowser_2 = QTextBrowser(self.main)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setGeometry(QRect(-10, 180, 191, 51))
        self.label = QLabel(self.main)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(120, 384, 131, 20))
        self.label.setAlignment(Qt.AlignCenter)
        self.start_ch = QPushButton(self.main)
        self.start_ch.setObjectName(u"start_ch")
        self.start_ch.setGeometry(QRect(360, 384, 88, 28))
        self.stop_ch = QPushButton(self.main)
        self.stop_ch.setObjectName(u"stop_ch")
        self.stop_ch.setGeometry(QRect(360, 422, 88, 28))
        self.stop_ch.setEnabled(False)
        self.custom_frag = QCheckBox(self.main)
        self.custom_frag.setObjectName(u"custom_frag")
        self.custom_frag.setGeometry(QRect(10, 150, 84, 24))
        self.custom_frag.setStyleSheet(u"")
        self.checker_end = QLineEdit(self.main)
        self.checker_end.setObjectName(u"checker_end")
        self.checker_end.setGeometry(QRect(60, 410, 41, 28))
        self.checker_end.setEnabled(False)
        self.checker_from = QLineEdit(self.main)
        self.checker_from.setObjectName(u"checker_from")
        self.checker_from.setGeometry(QRect(10, 410, 41, 28))
        self.checker_from.setEnabled(False)
        self.label_3 = QLabel(self.main)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(15, 384, 91, 16))
        self.tabWidget.addTab(self.main, "")
        self.textBrowser_2.raise_()
        log.raise_()
        self.label_2.raise_()
        self.righ_checkbox.raise_()
        self.frag_log.raise_()
        self.mci_checkbox.raise_()
        self.icell_checkbox.raise_()
        self.frag_checker.raise_()
        self.frag_status.raise_()
        self.label.raise_()
        self.start_ch.raise_()
        self.stop_ch.raise_()
        self.custom_frag.raise_()
        self.checker_end.raise_()
        self.checker_from.raise_()
        self.label_3.raise_()
        self.info = QWidget()
        self.info.setObjectName(u"info")
        self.textBrowser_3 = QTextBrowser(self.info)
        self.textBrowser_3.setObjectName(u"textBrowser_3")
        self.textBrowser_3.setGeometry(QRect(-10, -10, 651, 471))
        self.tabWidget.addTab(self.info, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.start_ch.clicked.connect(self.start_worker)

        self.retranslateUi(MainWindow)
        self.stop_ch.clicked.connect(self.stop_worker)

        self.retranslateUi(MainWindow)
        self.icell_checkbox.clicked.connect(self.IMR_checkbox)

        self.retranslateUi(MainWindow)
        self.mci_checkbox.clicked.connect(self.IMR_checkbox)

        self.retranslateUi(MainWindow)
        self.righ_checkbox.clicked.connect(self.IMR_checkbox)


        self.retranslateUi(MainWindow)
        self.custom_frag.clicked.connect(self.IMR_checkbox)

        self.tabWidget.setCurrentIndex(0)
    
    def log_write(self,wwlog):
        log.append(str(wwlog))

    def IMR_checkbox(self):
        if (self.icell_checkbox.isChecked()):
            Ui_MainWindow.num_fragment = 420
            Ui_MainWindow.checkbox_status = 1
            self.frag_status.setText(QCoreApplication.translate("MainWindow", u""+str(Ui_MainWindow.num_fragment), None))
            self.mci_checkbox.setEnabled(False)
            self.righ_checkbox.setEnabled(False)
            self.custom_frag.setEnabled(False)
            self.frag_status.setEnabled(False)

        elif (self.mci_checkbox.isChecked()):
            Ui_MainWindow.num_fragment = 550
            Ui_MainWindow.checkbox_status = 2
            self.frag_status.setText(QCoreApplication.translate("MainWindow", u""+str(Ui_MainWindow.num_fragment), None))
            self.righ_checkbox.setEnabled(False)
            self.icell_checkbox.setEnabled(False)
            self.custom_frag.setEnabled(False)
            self.frag_status.setEnabled(False)
            
        elif (self.righ_checkbox.isChecked()):
            Ui_MainWindow.num_fragment = 111
            Ui_MainWindow.checkbox_status = 3
            self.frag_status.setText(QCoreApplication.translate("MainWindow", u""+str(Ui_MainWindow.num_fragment), None))
            self.icell_checkbox.setEnabled(False)
            self.mci_checkbox.setEnabled(False)
            self.custom_frag.setEnabled(False)
            self.frag_status.setEnabled(False)
            
        elif (self.custom_frag.isChecked()):
            Ui_MainWindow.num_fragment = int(self.frag_status.text())
            Ui_MainWindow.checkbox_status = 4
            self.mci_checkbox.setEnabled(False)
            self.righ_checkbox.setEnabled(False)
            self.icell_checkbox.setEnabled(False)
            self.frag_status.setEnabled(False)

        else:
            self.mci_checkbox.setEnabled(True)
            self.righ_checkbox.setEnabled(True)
            self.icell_checkbox.setEnabled(True)
            self.custom_frag.setEnabled(True)
            self.frag_status.setEnabled(True)
        

        self.tabWidget.setCurrentIndex(0)
    

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Fragment Status", None))
        self.righ_checkbox.setText(QCoreApplication.translate("MainWindow", u"Rightell", None))
        self.frag_log.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.mci_checkbox.setText(QCoreApplication.translate("MainWindow", u"Hamrah-aval", None))
        log.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.icell_checkbox.setText(QCoreApplication.translate("MainWindow", u"irancell", None))
        self.frag_checker.setText(QCoreApplication.translate("MainWindow", u"Run Checker", None))
        self.frag_status.setText(QCoreApplication.translate("MainWindow", u""+str(self.num_fragment), None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Fragment Checker Status</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Fragment Checker", None))
        self.start_ch.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop_ch.setText(QCoreApplication.translate("MainWindow", u"Terminate", None))
        self.custom_frag.setText(QCoreApplication.translate("MainWindow", u"Custom", None))
        self.checker_end.setText(QCoreApplication.translate("MainWindow", u"450", None))
        self.checker_from.setText(QCoreApplication.translate("MainWindow", u"300", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Checker Range", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main), QCoreApplication.translate("MainWindow", u"main", None))
        self.textBrowser_3.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /> \u0628\u0631\u0627\u06cc \u06a9\u0627\u0631\u0628\u0631\u0627\u0646 \u0627\u0646\u062f\u0631\u0648\u06cc\u062f MahsaNG \u062f\u0631\u06cc\u0627\u0641\u062a \u06a9\u0627\u0646\u0641\u06cc\u06af \u0631\u0627\u06cc\u06af\u0627\u0646 \u0628\u0627 \u0627\u0633\u062a\u0641\u0627\u062f\u0647 \u0627\u0632 \u0628\u0631\u0646\u0627\u0645\u0647</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; text-decoration: underline; color:#005"
                        "7ae;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#55aaff;\">\u0644\u06cc\u0646\u06a9 \u06af\u0648\u06af\u0644 \u067e\u0644\u06cc</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#55aaff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">https://play.google.com/store/apps/details?id=com.MahsaNet.MahsaNG</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; text-decoration: underline;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0"
                        "px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; text-decoration: underline;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#00aaff;\"> \u062f\u0627\u0646\u0644\u0648\u062f \u0645\u0633\u062a\u0642\u06cc\u0645</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#00aaff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline; color:#000102;\">https://github.com/GFW-knocker/MahsaNG/releases</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; text-decoration: underline; c"
                        "olor:#000102;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; text-decoration: underline; color:#00aaff;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; text-decoration: underline; color:#00aaff;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600; color:#00060c;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    By : Kiyan</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.info), QCoreApplication.translate("MainWindow", u"info", None))
        pass
    # retranslateUi

    thread = {}

    def start_worker(self):
        self.start_ch.setEnabled(False)
        if (Ui_MainWindow.num_fragment == 0) or (Ui_MainWindow.num_fragment == None):
            counter = 0
            while (counter<5):
                app.processEvents()
                pr = Ui_MainWindow()
                pr.log_write(' ** Enter Fragment Number In Fragment Status Box ** ')
                pr.log_write(" */*/ Exiting From Program */*/")
                counter += 1
                time.sleep(1)
            exit()
        if (Ui_MainWindow.checkbox_status == 1):
            self.icell_checkbox.setEnabled(False)
        elif (Ui_MainWindow.checkbox_status == 2):
            self.mci_checkbox.setEnabled(False)
        elif (Ui_MainWindow.checkbox_status == 3):
            self.righ_checkbox.setEnabled(False)
        elif(Ui_MainWindow.checkbox_status == 4):
            self.custom_frag.setEnabled(False)
        self.thread[1] = ThreadClass(parent=None,index=1)
        pr = Ui_MainWindow()
        pr.log_write('Start Listening On 127.0.0.1:%s' % str(listen_PORT))
        pr.log_write("Fragment sleep : %s" % (fragment_sleep))
        #pr.log_write("Num Fragment is : %s" % (Ui_MainWindow.num_fragment))
        self.thread[1].start()
        #self.thread[1].any_signal.connect(self.my_function)
        self.stop_ch.setEnabled(True)


    def stop_worker(self):
        self.thread[1].stop()
        self.start_ch.setEnabled(True)


class ThreadClass(QThread,Ui_MainWindow):
    #any_signal = QtCore.pyqtSignal(int)
    def __init__(self,parent=None,index=0):

        super(ThreadClass,self).__init__(parent)
        self.index = index
        self.is_running = True
        
    def run(self):
        #print('starting thread.... \n',self.index)
        while True:
            app.processEvents()
            #print('Debug-Testing [1]')
            ThreadedServer('',listen_PORT).listen()
            time.sleep(0.5)
                

    def stop(self):
        self.is_running = False
        #print(" \n Stop thread... \n")
        self.terminate()

DNS_url = 'https://cloudflare-dns.com/dns-query?dns='
# DNS_url = 'https://8.8.4.4/dns-query?dns='      # blocked?
# DNS_url = 'https://8.8.8.8/dns-query?dns='      # blocked?
# DNS_url = 'https://1.1.1.1/dns-query?dns='      # blocked?
# DNS_url = 'https://dns.google/dns-query?dns='              # blocked?
# DNS_url = 'https://doh.opendns.com/dns-query?dns='           # blocked?
# DNS_url = 'https://secure.avastdns.com/dns-query?dns='      # blocked?
# DNS_url = 'https://doh.libredns.gr/dns-query?dns='          # blocked?
# DNS_url = 'https://dns.electrotm.org/dns-query?dns='        # DNS server inside iran
# DNS_url = 'https://dns.bitdefender.net/dns-query?dns='
# DNS_url = 'https://cluster-1.gac.edu/dns-query?dns='



offline_DNS = {

################## DNS over HTTPS IP Address (leave it intact , it must Exist) ######################
# 'cloudflare-dns.com':'1.1.1.1',  # IP filtered
# 'cloudflare-dns.com':'172.67.128.43',   # any cludflare ip can be used for cloudflare DoH 
# 'cloudflare-dns.com':'64.68.192.137',   
'cloudflare-dns.com':'203.32.120.226',


'dns.google':'8.8.8.8',    # IP filtered
'doh.opendns.com':'208.67.222.222',    
'secure.avastdns.com':'185.185.133.66',  
'doh.libredns.gr':'116.202.176.26',           
'dns.electrotm.org':'78.157.42.100',
'dns.bitdefender.net':'34.84.232.67',
'cluster-1.gac.edu':'138.236.128.101',
##########################################################################




# ################# twitter working pack ###################
# 'ocsp.digicert.com': '192.229.211.108',

'api.twitter.com': '104.244.42.66',
'twitter.com': '104.244.42.1',
'pbs.twimg.com': '93.184.220.70',
'abs-0.twimg.com': '104.244.43.131',
'abs.twimg.com': '152.199.24.185', 
'video.twimg.com': '192.229.220.133', 
't.co': '104.244.42.69',
'ton.local.twitter.com':'104.244.42.1',
# ##########################################################



# ################# Instagram whatsapp facebook working pack ###################
'instagram.com': '163.70.128.174',
'www.instagram.com': '163.70.128.174',
'static.cdninstagram.com': '163.70.132.63',
'scontent.cdninstagram.com':'163.70.132.63',
'privacycenter.instagram.com': '163.70.128.174',
'help.instagram.com': '163.70.128.174',
'l.instagram.com':'163.70.128.174',


'e1.whatsapp.net':'163.70.128.60',
'e2.whatsapp.net':'163.70.128.60',
'e3.whatsapp.net':'163.70.128.60',
'e4.whatsapp.net':'163.70.128.60',
'e5.whatsapp.net':'163.70.128.60',
'e6.whatsapp.net':'163.70.128.60',
'e7.whatsapp.net':'163.70.128.60',
'e8.whatsapp.net':'163.70.128.60',
'e9.whatsapp.net':'163.70.128.60',
'e10.whatsapp.net':'163.70.128.60',
'e11.whatsapp.net':'163.70.128.60',
'e12.whatsapp.net':'163.70.128.60',
'e13.whatsapp.net':'163.70.128.60',
'e14.whatsapp.net':'163.70.128.60',
'e15.whatsapp.net':'163.70.128.60',
'e16.whatsapp.net': '163.70.128.60',

'dit.whatsapp.net': '185.60.219.60',
'g.whatsapp.net': '185.60.218.54',
'wa.me':'185.60.219.60',

'web.whatsapp.com':'31.13.83.51',
'whatsapp.net':'31.13.83.51',
'whatsapp.com':'31.13.83.51',
'cdn.whatsapp.net':'31.13.83.51',
'snr.whatsapp.net':'31.13.83.51', 

'static.xx.fbcdn.net': '31.13.75.13',
'scontent-mct1-1.xx.fbcdn.net':'31.13.75.13',
'video-mct1-1.xx.fbcdn.net': '31.13.75.13',
'video.fevn1-2.fna.fbcdn.net': '185.48.241.146',
'video.fevn1-4.fna.fbcdn.net': '185.48.243.145',
'scontent.xx.fbcdn.net':'185.48.240.146',
'scontent.fevn1-1.fna.fbcdn.net': '185.48.240.145',
'scontent.fevn1-2.fna.fbcdn.net': '185.48.241.145',
'scontent.fevn1-3.fna.fbcdn.net': '185.48.242.146',
'scontent.fevn1-4.fna.fbcdn.net': '185.48.243.147',


'connect.facebook.net': '31.13.84.51',
'facebook.com':'31.13.65.49',
'developers.facebook.com': '31.13.84.8',

'about.meta.com': '163.70.128.13',
'meta.com':'163.70.128.13',
# ##########################################################


######################## Twitch working pack ######################



# ################# GooglePlay working pack ###################

# ##########################################################


##################### youtube working pack ################################
'ocsp.pki.goog': '172.217.16.195',
'googleads.g.doubleclick.net': '45.157.177.108',
'fonts.gstatic.com': '142.250.185.227',
'rr2---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.141',
'jnn-pa.googleapis.com': '45.157.177.108',
'static.doubleclick.net': '202.61.195.218', 
'rr4---sn-hju7en7k.googlevideo.com': '74.125.167.74',
'rr1---sn-hju7en7r.googlevideo.com': '74.125.167.87',
'play.google.com': '142.250.184.238',
'rr3---sn-vh5ouxa-hjuz.googlevideo.com': '134.0.218.206', 
'rr3---sn-hju7enel.googlevideo.com': '74.125.98.40',
'download.visualstudio.microsoft.com': '68.232.34.200',
'ocsp.pki.goog': '172.217.16.195',
'i.ytimg.com': '142.250.186.150',
'rr2---sn-hju7enel.googlevideo.com': '74.125.98.39',
'rr2---sn-hju7en7k.googlevideo.com': '74.125.167.72', 
'googleads.g.doubleclick.net': '45.157.177.108',
'rr3---sn-4g5lznl6.googlevideo.com': '74.125.173.40', 
'jnn-pa.googleapis.com': '89.58.57.45', 
'rr3---sn-hju7en7k.googlevideo.com': '74.125.167.73',
'rr1---sn-hju7enll.googlevideo.com': '74.125.98.6',
'rr6---sn-hju7en7r.googlevideo.com': '74.125.167.92',
'play.google.com': '216.58.212.174',
'www.gstatic.com': '142.250.185.99', 
'apis.google.com': '172.217.23.110',
'adservice.google.com': '202.61.195.218',
'mail.google.com': '142.250.186.37', 
'accounts.google.com': '172.217.16.205', 
'lh3.googleusercontent.com': '193.26.157.66',
'accounts.youtube.com': '172.217.16.206',
'ssl.gstatic.com': '142.250.184.195', 
'fonts.gstatic.com': '172.217.23.99', 
'rr4---sn-hju7enll.googlevideo.com': '74.125.98.9',
'rr2---sn-hju7enll.googlevideo.com': '74.125.98.7',
'rr1---sn-hju7enel.googlevideo.com': '74.125.98.38',
'rr5---sn-vh5ouxa-hjuz.googlevideo.com': '134.0.218.208', 
'i1.ytimg.com': '172.217.18.14',
'plos.org': '162.159.135.42', 
'fonts.googleapis.com': '89.58.57.45',
'genweb.plos.org': '104.26.1.141',
'static.ads-twitter.com': '146.75.120.157',
'www.google-analytics.com': '142.250.185.174',
'rr1---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.140',
'rr5---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.144',
'rr3---sn-hju7enel.googlevideo.com': '74.125.98.40',
'rr5---sn-nv47zn7y.googlevideo.com': '173.194.15.74', 
'rr1---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.140',
'safebrowsing.googleapis.com': '202.61.195.218',
'static.doubleclick.net': '193.26.157.66',
'rr5---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.144', 
'rr1---sn-hju7en7r.googlevideo.com': '74.125.167.87',
'rr4---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.143',
'rr4---sn-hju7en7r.googlevideo.com': '74.125.167.90',
'r1---sn-hju7enel.googlevideo.com': '74.125.98.38', 
'rr1---sn-nv47zn7r.googlevideo.com': '173.194.15.38',
'rr2---sn-vh5ouxa-hjuz.googlevideo.com': '134.0.218.205', 
'rr4---sn-nv47zn7r.googlevideo.com': '173.194.15.41',
'rr4---sn-hju7en7r.googlevideo.com': '74.125.167.90',

'www.google.com': '142.250.186.36',
# 'www.google.com': '216.239.38.120',
'youtube.com':'142.250.185.78',
'youtu.be':'142.250.185.174',
'www.youtube.com':'142.250.185.238',
'i.ytimg.com':'142.250.185.86',

# 'yt3.ggpht.com': '64.233.165.198',   # filtered
# 'yt3.ggpht.com': '142.250.179.161',  # filtered
# 'yt3.ggpht.com': '142.250.186.65',   # sometimes work
'yt3.ggpht.com': '142.250.186.36',   # most of times work
#######################################################



}


# ignore description below , its for old code , just leave it intact.
my_socket_timeout = 8 # default for google is ~21 sec , recommend 60 sec unless you have low ram and need close soon
first_time_sleep = 0.1 # speed control , avoid server crash if huge number of users flooding
accept_time_sleep = 0.01 # avoid server crash on flooding request -> max 100 sockets per second


DNS_cache = {}      # resolved domains
IP_DL_traffic = {}  # download usage for each ip
IP_UL_traffic = {}  # upload usage for each ip


class DNS_over_Fragment:
    def __init__(self):
        self.url = DNS_url
        self.req = requests.session()              
        self.fragment_proxy = {
        'https': 'http://127.0.0.1:'+str(listen_PORT)
        }
        


    def query(self,server_name):     

        offline_ip = offline_DNS.get(server_name,None)
        if(offline_ip!=None):
            print('offline DNS -->',server_name,offline_ip)
            return offline_ip
        
        cache_ip = DNS_cache.get(server_name,None)
        if(cache_ip!=None):
            print('cached DNS -->',server_name,cache_ip)
            return cache_ip

        quary_params = {
            # 'name': server_name,    # no need for this when using dns wire-format , cause 400 err on some server
            'type': 'A',
            'ct': 'application/dns-message',
            }
        

        print(f'online DNS Query',server_name)        
        try:
            query_message = dns.message.make_query(server_name,'A')
            query_wire = query_message.to_wire()
            query_base64 = base64.urlsafe_b64encode(query_wire).decode('utf-8')
            query_base64 = query_base64.replace('=','')    # remove base64 padding to append in url            

            query_url = self.url + query_base64
            ans = self.req.get( query_url , params=quary_params , headers={'accept': 'application/dns-message'} , proxies=self.fragment_proxy , verify=(not allow_insecure))
            
            # Parse the response as a DNS packet
            if ans.status_code == 200 and ans.headers.get('content-type') == 'application/dns-message':
                answer_msg = dns.message.from_wire(ans.content)

                resolved_ip = None
                for x in answer_msg.answer:
                    if (x.rdtype == dns.rdatatype.A):
                        resolved_ip = x[0].address    # pick first ip in DNS answer
                        DNS_cache[server_name] = resolved_ip                        
                        print("################# DNS Cache is : ####################")
                        print(DNS_cache)         # print DNS cache , it usefull to track all resolved IPs , to be used later.
                        print("#####################################################")
                        break
                
                print(f'online DNS --> Resolved {server_name} to {resolved_ip}')                
                return resolved_ip
            else:
                print(f'Error: {ans.status_code} {ans.reason}')
        except Exception as e:
            print(repr(e))
        

class ThreadedServer(object):
    
    def __init__(self, host, port):
        self.DoH = DNS_over_Fragment()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(128)  # up to 128 concurrent unaccepted socket queued , the more is refused untill accepting those.
        while True:
            client_sock , client_addr = self.sock.accept()
            client_sock.settimeout(my_socket_timeout)
            time.sleep(accept_time_sleep)   # avoid server crash on flooding request
            thread_up = threading.Thread(target = self.my_upstream , args =(client_sock,) )
            thread_up.daemon = True   #avoid memory leak by telling os its belong to main program , its not a separate program , so gc collect it when thread finish
            thread_up.start()
    


    def handle_client_request(self,client_socket):
        # Receive the CONNECT request from the client
        data = client_socket.recv(16384)
        

        if(data[:7]==b'CONNECT'):            
            server_name , server_port = self.extract_servername_and_port(data)            
        elif( (data[:3]==b'GET') 
            or (data[:4]==b'POST') 
            or (data[:4]==b'HEAD')
            or (data[:7]==b'OPTIONS')
            or (data[:3]==b'PUT') 
            or (data[:6]==b'DELETE') 
            or (data[:5]==b'PATCH') 
            or (data[:5]==b'TRACE') ):  

            q_line = str(data).split('\r\n')
            q_req = q_line[0].split()
            q_method = q_req[0]
            q_url = q_req[1]
            q_url = q_url.replace('http://','https://')
            print('************************@@@@@@@@@@@@***************************')
            print('redirect',q_method,'http to HTTPS',q_url)          
            response_data = 'HTTP/1.1 302 Found\r\nLocation: '+q_url+'\r\nProxy-agent: MyProxy/1.0\r\n\r\n'            
            client_socket.sendall(response_data.encode())
            client_socket.close()            
            return None
        else:
            print('Unknown Method',str(data[:10]))            
            response_data = b'HTTP/1.1 400 Bad Request\r\nProxy-agent: MyProxy/1.0\r\n\r\n'
            client_socket.sendall(response_data)
            client_socket.close()            
            return None

        
        print(server_name,'-->',server_port)

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.settimeout(my_socket_timeout)
            server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)   #force localhost kernel to send TCP packet immediately (idea: @free_the_internet)

            try:
                socket.inet_aton(server_name)
                # print('legal IP')
                server_IP = server_name
            except socket.error:
                # print('Not IP , its domain , try to resolve it')
                server_IP = self.DoH.query(server_name)
            

            try:
                server_socket.connect((server_IP, server_port))
                # Send HTTP 200 OK
                response_data = b'HTTP/1.1 200 Connection established\r\nProxy-agent: MyProxy/1.0\r\n\r\n'            
                client_socket.sendall(response_data)
                return server_socket
            except socket.error:
                print("@@@ "+server_IP+":"+str(server_port)+ " ==> filtered @@@")
                # Send HTTP ERR 502
                response_data = b'HTTP/1.1 502 Bad Gateway (is IP filtered?)\r\nProxy-agent: MyProxy/1.0\r\n\r\n'
                client_socket.sendall(response_data)
                client_socket.close()
                server_socket.close()
                return server_IP

            
        except Exception as e:
            print(repr(e))
            # Send HTTP ERR 502
            response_data = b'HTTP/1.1 502 Bad Gateway (Strange ERR?)\r\nProxy-agent: MyProxy/1.0\r\n\r\n'
            client_socket.sendall(response_data)
            client_socket.close()
            server_socket.close()
            return None


    def my_upstream(self, client_sock):
        first_flag = True
        backend_sock = self.handle_client_request(client_sock)

        if(backend_sock==None):
            client_sock.close()
            return False
        
        if( isinstance(backend_sock,str) ):
            this_ip = backend_sock
            if(this_ip not in IP_UL_traffic):
                IP_UL_traffic[this_ip] = 0
                IP_DL_traffic[this_ip] = 0
            client_sock.close()
            return False

        
        this_ip = backend_sock.getpeername()[0]
        if(this_ip not in IP_UL_traffic):
            IP_UL_traffic[this_ip] = 0
            IP_DL_traffic[this_ip] = 0
        
        
        while True:
            try:
                if( first_flag == True ):                
                    first_flag = False

                    time.sleep(first_time_sleep)   # speed control + waiting for packet to fully recieve
                    data = client_sock.recv(16384)
                    #print('len data -> ',str(len(data)))                
                    #print('user talk :')

                    if data:                                                                                            
                        thread_down = threading.Thread(target = self.my_downstream , args = (backend_sock , client_sock) )
                        thread_down.daemon = True
                        thread_down.start()
                        # backend_sock.sendall(data)    
                        send_data_in_fragment(data,backend_sock)
                        IP_UL_traffic[this_ip] = IP_UL_traffic[this_ip] + len(data)

                    else:                   
                        raise Exception('cli syn close')

                else:
                    data = client_sock.recv(16384)
                    if data:
                        backend_sock.sendall(data)  
                        IP_UL_traffic[this_ip] = IP_UL_traffic[this_ip] + len(data)                      
                    else:
                        raise Exception('cli pipe close')
                    
            except Exception as e:
                #print('upstream : '+ repr(e) )
                time.sleep(2) # wait two second for another thread to flush
                client_sock.close()
                backend_sock.close()
                return False



            
    def my_downstream(self, backend_sock , client_sock):
        this_ip = backend_sock.getpeername()[0]        

        first_flag = True
        while True:
            try:
                if( first_flag == True ):
                    first_flag = False            
                    data = backend_sock.recv(16384)
                    if data:
                        client_sock.sendall(data)
                        IP_DL_traffic[this_ip] = IP_DL_traffic[this_ip] + len(data)
                    else:
                        raise Exception('backend pipe close at first')
                    
                else:
                    data = backend_sock.recv(16384)
                    if data:
                        client_sock.sendall(data)
                        IP_DL_traffic[this_ip] = IP_DL_traffic[this_ip] + len(data)
                    else:
                        raise Exception('backend pipe close')
            
            except Exception as e:
                #print('downstream '+backend_name +' : '+ repr(e)) 
                time.sleep(2) # wait two second for another thread to flush
                backend_sock.close()
                client_sock.close()
                return False



    def extract_servername_and_port(self,data):        
        host_and_port = str(data).split()[1]
        host,port = host_and_port.split(':')
        return (host,int(port)) 



def merge_all_dicts():
    full_DNS = {**DNS_cache, **offline_DNS}  # merge two dict , need python 3.5 or up
    inv_DNS = { v:k for k,v in full_DNS.items()}  # inverse mapping to look for domain given ip
    stats = {}
    for ip in IP_UL_traffic:  
        up = round(IP_UL_traffic[ip]/(1024.0),3)
        down = round(IP_DL_traffic[ip]/(1024.0),3)
        host = inv_DNS.get(ip,'?')
        if( (down<1.0) ):  # download below 1KB
            maybe_filter = ' yes'
        else:
            maybe_filter = '-------'

        su = f'UL={up} KB:'
        sd = f'DL={down} KB:'        
        sf = f'filtered={maybe_filter}:'
        sh = f'Host={host}:'
        stats[ip] = ':'+su+sd+sf+sh
    return stats



# only run in separate thread
def log_writer():
    file_name = 'DNS_IP_traffic_info.txt'
    BASE_DIR = Path(__file__).resolve().parent
    log_file_path = os.path.join(BASE_DIR,file_name)
    
    with open(log_file_path, "w") as f:
        while True:
            time.sleep(log_every_N_sec)
            all_stats_info = merge_all_dicts()           
            f.seek(0)
            f.write('\n########### new DNS resolved : ##############\n')
            f.write(str(DNS_cache).replace(',',',\n'))
            f.write('\n#############################################\n')
            f.write('\n########### ALL INFO : ######################\n')
            f.write(str(all_stats_info).replace('\'','').replace(',','\n').replace(':','\t'))
            f.write('\n#############################################\n')
            f.flush()
            f.truncate()
            print("info file writed to",f.name )



def start_log_writer():
    thread_log = threading.Thread(target = log_writer , args = () )
    thread_log.daemon = True
    thread_log.start()





def send_data_in_fragment(data , sock):
    num_fragment = Ui_MainWindow.num_fragment
    L_data = len(data)
    indices = random.sample(range(1,L_data-1), num_fragment-1)
    indices.sort()
    # print('indices=',indices)

    i_pre=0
    for i in indices:
        fragment_data = data[i_pre:i]
        i_pre=i
        # print('send ',len(fragment_data),' bytes')                        
        
        # sock.send(fragment_data)
        sock.sendall(fragment_data)
        
        time.sleep(fragment_sleep)
    
    fragment_data = data[i_pre:L_data]
    sock.sendall(fragment_data)
    print('----------finish------------')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())