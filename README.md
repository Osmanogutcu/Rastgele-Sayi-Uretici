# Rastgele-Sayi-Uretici
# 🌑 GÖLGE-128 (Shadow-128) Şifreleme Algoritması

> **"Kriptografik Algoritma Geliştirme ve Analizi Projesi"**

Bu proje, **GÖLGE-128 (Shadow-128)** adı verilen özgün bir blok şifreleme algoritmasının tasarımını, Python ile uygulanmasını ve güvenlik analizini kapsar. Algoritma, SPN (Substitution-Permutation Network) mimarisi üzerine kurgulanmıştır.
Şifreli Veri (Hex):75A1FEECCA37DB694C09DB4C2D587E88
---
Geliştirici:Osman Kerim Ögütçü
## 📋 Proje Özeti (Deney Föyü Kapsamı)

Bu çalışma 3 ana aşamadan oluşmaktadır:
1.  **Tasarım:** Algoritmanın matematiksel modelinin ve akış şemasının oluşturulması.
2.  **Kodlama:** Tasarımın Python dili ile `Sifrele` ve `Desifrele` fonksiyonlarına dökülmesi.
3.  **Analiz (Kırılma):** Algoritmanın zayıf yönlerinin (Kriptanaliz) test edilmesi.

## 🛠 Teknik Özellikler

| Özellik | Değer |
| :--- | :--- |
| **Algoritma Tipi** | Simetrik Blok Şifreleme (SPN) |
| **Blok Boyutu** | 128-Bit (16 Byte) |
| **Anahtar Boyutu** | 128-Bit |
| **Tur Sayısı** | 10 Tur (Rounds) |
| **Dil** | Python 3 |

## 🧮 Algoritma Mantığı

Algoritma, Shannon'un **Karıştırma (Confusion)** ve **Yayılma (Diffusion)** ilkelerini sağlamak için her turda şu 3 temel işlemi uygular:

### 1. İkame Katmanı (SubBytes)
Her byte ($b$) için doğrusal olmayan matematiksel bir dönüşüm uygulanır. Bu işlem S-Box görevi görür:
$$S(b) = (b \times 5 + 13) \pmod{256}$$

### 2. Permütasyon Katmanı (ShiftRows)
16 Byte'lık veri bloğu 4x4 matris olarak düşünülür ve satırlar sola kaydırılarak bitlerin dağılması sağlanır:
* **1. Satır:** Sabit
* **2. Satır:** 1 Byte Sola
* **3. Satır:** 2 Byte Sola
* **4. Satır:** 3 Byte Sola

### 3. Anahtar Genişletme (Key Schedule)
Ana anahtardan 10 adet tur anahtarı üretilir. Her turda anahtar **sola 3 bit kaydırılır (rotate)** ve tur sayacı ile XOR işlemine girer.

---

## 🚀 Kurulum ve Kullanım

Proje dosyası `golge128_final.py` içerisinde hem şifreleme/deşifreleme fonksiyonları hem de otomatik test senaryoları bulunur.

### 1. Çalıştırma
Python yüklü bir terminalde şu komutu girin:
```bash
python golge128_final.py
