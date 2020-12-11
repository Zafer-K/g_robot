import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow


# Tanımlamalar
sayac = 0
x1 = 0
x2 = 0
y1 = 0
y2 = 0
secim = ""
sag = 0
aralik_deger = 0

qtcreator_file = "son.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.color = QColor(Qt.green)

        # Durum Label
        self.lbl_durum.setText("")

        # Combobox ların değeri değiştiğinde bağlanacakları fonksiyonlar
        self.cmbbx_mod.currentTextChanged.connect(self.mod_secim)
        self.cmbbx_olcek.currentTextChanged.connect(self.olcek_secim)

        # GroupBox ların başlangıçtaki durumları
        self.grpbx_manuel.setEnabled(False)
        self.grpbx_harita.setEnabled(False)

        # Slider kullanıldığında gitmesi gereken yeri tanımlama
        self.slider_hiz.valueChanged.connect(self.hiz_degisim)

        # Çizimde mouse sol buton kullanımı için label da hata gösterimi
        self.lbl_cizim.setText("Çizime başlamak için\nfarenin sol tuşuna basınız.")

        # Spinbox ilk değer 0 olarak ayarlandı
        self.spnbx_aralik.setValue(0)

        # Ayarla butonu
        self.btn_ayarla.clicked.connect(self.ayarla_click)
        
        # Uygulama butonları aktivitesi yapılıyor
        # İleri butonu için tmm
        self.btn_ileri.clicked.connect(self.ileri_click)
        # Geri butonu
        self.btn_geri.clicked.connect(self.geri_click)
        # Sağa dön butonu
        self.btn_sag.clicked.connect(self.sag_click)
        # Sola dön butonu
        self.btn_sol.clicked.connect(self.sol_click)
        # Dur butonu
        self.btn_dur.clicked.connect(self.dur_click)
        
        # Önceki deneme
        # İp adresi line_edit
        # self.line_ip.editingFinished.connect(self.ip_adresi)

        # İp adresini alıyoruz
        self.ip_adresi = self.line_ip.editingFinished.connect(self.ip_add)
    # IP adresi alınması
    def ip_add(self):
        self.ip_adresi = self.line_ip.text()
    
    # Ayarla Butonu işlevi
    def ayarla_click(self):
        # Eğer http sunucusundan cevap geliyorsa ayarlandı diyecek 
        # Gelmiyorsa bağlanılmadı diyecek
        self.lbl_durum.setText("Bağlandı...")

    # Dur butonu
    def dur_click(self):
        self.dur = requests.get("http://" + self.ip_adresi + "/dur")

    # İleri butonunun fonksiyonu
    def ileri_click(self):
        self.ileri = requests.get("http://" + self.ip_adresi + "/ileri_git")
        #cevap = self.ileri.status_code
        #print(cevap)
        #print(str(self.ip_add) + " adresine ileri butonuna tıklanıldı bilgisi gönderildi.")

    # Geri butonunun fonksiyonu
    def geri_click(self):
        self.geri = requests.get("http://" + self.ip_adresi + "/geri_git")
        #cevap = self.geri.status_code
        #print(cevap)
        #print(str(self.ip_add) + " adresine geri butonuna tıklanıldı bilgisi gönderildi.")
    
    # Sağ butonun fonksiyonu
    def sag_click(self):
        self.sag = requests.get("http://" + self.ip_adresi + "/saga_don")
        #cevap = self.sag.status_code
        #print(cevap)
        #print(str(self.ip_add) + " adresine sağa dön butonuna tıklanıldı bilgisi gönderildi.")
   
   # Sol butonun fonksiyonu
    def sol_click(self):
        self.sol = requests.get("http://" + self.ip_adresi + "/sola_don")
        #cevap = self.sol.status_code
        #print(cevap)
        #print(str(self.ip_add) + " adresine sola dön butonuna tıklanıldı bilgisi gönderildi.")

    # Mod seçim fonksiyonu
    def mod_secim(self):
        global secim
        secim = self.cmbbx_mod.currentText()
        self.grpbx_manuel.setEnabled(False)
        self.grpbx_harita.setEnabled(False)
        print(secim)

        if(secim == "Seçiniz"):
            print("İşlem yapabilmek için mod seçmelisiniz")

        elif(secim == "Harita Modu"):
            self.grpbx_harita.setEnabled(True)
            self.lbl_durum.setText("Harita Modu Seçildi...")
            # Aralık değeri değiştirilmesi
            self.spnbx_aralik.valueChanged.connect(self.aralik_degisim)
            
            self.mod = requests.get("http://" + self.ip_adresi + "/harita_modu")
            
        elif(secim == "Manuel Mod"):
            self.grpbx_manuel.setEnabled(True)
            self.lbl_durum.setText("Manuel Mod Seçildi..")
            self.mod = requests.get("http://" + self.ip_adresi + "/manuel_mod")
   
    # Ölçek Seçim Fonksiyonu
    def olcek_secim(self):
        olsec = self.cmbbx_olcek.currentText()
        print("Seçim = " + olsec)
        # olces degişkeninin başlangıçtan itibaren ilk iki terimine bakılıp karar veriliyor
        if(olsec[:2] == "mm"):
            print("Seçim mm olarak ayarlanmıştır")
            self.lbl_olcek.setText("mm")
        elif(olsec[:2] == "cm"):
            print("Seçim cm olarak ayarlanmıştır..")
            self.lbl_olcek.setText("cm")
        elif(olsec[:2] == "m "):
            print("Seçim m olarak ayarlanmıştır..")
            self.lbl_olcek.setText("m")
        else:
            print("Seçim yapmadınız seçim yapmanız gerekmektedir...")

    # Hız değişim fonksiyonu
    def hiz_degisim(self):
        deger = self.slider_hiz.value()
        print("Slider değeri: "+ str(deger))
        self.lbl_hiz.setText(str(deger))
        ## Hız ayarı her değiştiğinde arduinoya veri göndermek için kullanıldı
        self.araba_hiz = requests.get("http://" + self.ip_adresi + "/hiz_ayarla=" + str(deger))
        #cevap = self.geri.status_code
        #print(cevap)
        #print(str(self.ip_add) + " adresinde hız ayarlaması yapıldı.")

    def aralik_degisim(self):
        global aralik_deger
        aralik_deger = self.spnbx_aralik.value()
        if(aralik_deger == 0):
            self.btn_link.setEnabled(False)
        else:
            self.btn_link.setEnabled(True)
        print("Aralık değeri : " + str(self.spnbx_aralik.value()))

        # Buraya arduinoya gidecek veriler için kodlar yazılacak

    # X1 ve Y1 değerlerinin alınması
    def birinci_konum(self):
        deger_x = x1 / aralik_deger
        deger_y = y1 / aralik_deger
        self.lbl_x1.setText(str(deger_x))
        self.lbl_y1.setText(str(deger_y))

    def ikinci_konum(self):
        deger_x = x2 / aralik_deger
        deger_y = y2 / aralik_deger
        self.lbl_x2.setText(str(deger_x))
        self.lbl_y2.setText(str(deger_y))
       
    # Mouse İşlemlerinin yapıldığı fonksiyon
    def mousePressEvent(self, QMouseEvent = None):
        # Seçim harita modu ise ve mouse un sol butonuna tıklanıyorsa ve tanımlı aralıkta ise
        # Noktalar tanımlanıp
        # Çizdirme işlemi başlatılıyor
        global sag
        if((secim == "Harita Modu") & (QMouseEvent.button() == Qt.LeftButton) & (QMouseEvent.x() > 320) & (QMouseEvent.x() < 601) & (QMouseEvent.y() >220) & (QMouseEvent.y() < 381)):
            # Global olarak tanımlandı ki diğer fonksiyonlarda ulaşılabilsinler
            global sayac, x1, x2, y1, y2
            sayac += 1
            self.lbl_cizim.setText(str(sayac) + ". nokta ayarlandı.")
            #print("Tanımlı aralık")
            # İlk nokta tanımlaması yapılır
            if(aralik_deger == 0):
                sayac = 0
                self.lbl_cizim.setText("Aralık değerini değiştirmelisiniz")
            else:
                #self.lbl_cizim.setText("Aralık değeri ayarlandı...")
                
                if(sayac == 1):
                    x1 = QMouseEvent.x()
                    y1 = QMouseEvent.y()
                    # Konsolda görmek için
                    print("X1= "+ str(x1))
                    print("Y1= "+ str(y1))
                    # Arayüzde görmek için fonksiyon ile birlikte çağırıyoruz
                    self.birinci_konum()
                # İkinci nokta tanımlaması yapılır
                elif(sayac == 2):
                    x2 = QMouseEvent.x()
                    y2 = QMouseEvent.y()
                    # Konsolda görmek için
                    print("X2= "+ str(x2))
                    print("Y2= "+ str(y2))
                    # Arayüzde görmek için fonksiyonu çağırdık
                    self.ikinci_konum()
                    self.lbl_cizim.setText(str(sayac) + ". nokta ayarlandı.\nÇizdirmek için birkez daha tıklayınız..")
            
                # Buraya bakılacakkkkkkkkkkkkkkkkkkkkkk
                elif((sayac == 3) & (secim == "Harita Modu")):
                    qp.begin(self)
                    self.changePoints()
                    self.lbl_cizim.setText("Yol belirlendi.")
                    sayac = 0
                else:
                    sayac = 0
                        
                print("Sayac = " + str(sayac))
        elif((secim != "Harita Modu") & (QMouseEvent.button() == Qt.LeftButton)):
            self.lbl_cizim.setText("Çizime başlamak için\nHarita Modu seçilmelidir.")

        elif(QMouseEvent.button() != Qt.LeftButton):
            self.lbl_cizim.setText("Lütfen sol butona tıklayınız.")
            
        else:
            self.lbl_cizim.setText("İşlem yapabilmek için\ntanımlı aralıkta olmalısınız.")
            #self.lbl_cizim.setText("Yanlış tuşa tıklanıldı.")
            sayac = 0

    def paintEvent(self, event):
        global qp
        qp = QtGui.QPainter(self)
        #qp.begin(self)
        print("Paint Event çalıştı..")
        print("DrawCizgi ye geçildi")
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(QPen(QColor(Qt.red), 3, Qt.SolidLine))
        qp.setBrush(self.color)
        qp.drawLine(
                    QtCore.QPoint(x1, y1),
                    QtCore.QPoint(x2, y2)
        )
        #print("X1 = " + str(x1) + " Y1 = " + str(y1))
        qp.end()
        print("DrawCizgi bitti.")
        
                
   # Noktaları güncellemek için kullandık
    def changePoints(self):
        qp.drawLine(
            QtCore.QPoint(x1, y1),
            QtCore.QPoint(x2, y2)
        )
        print("Noktalar ayarlandı...")
        self.update()

# Penceremizi oluşturduğumuz fonksiyon
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
