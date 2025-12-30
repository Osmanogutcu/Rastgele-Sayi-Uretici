# Rastgele-Sayi-Uretici
# 🌑 GÖLGE-128 (Shadow-128)

> **"Gölge, gerçeği takip eder ama asla ele vermez."**

**GÖLGE-128**, SPN (Substitution-Permutation Network) mimarisi üzerine kurgulanmış, modern blok şifreleme prensiplerini gösteren akademik bir kriptografi projesidir. Standart S-Box tabloları yerine işlemci dostu matematiksel dönüşümler kullanır.

---

## 🛠 Teknik Özellikler

| Özellik | Değer |
| :--- | :--- |
| **Algoritma Türü** | Simetrik Blok Şifreleme (SPN) |
| **Blok Boyutu** | 128-Bit (16 Byte) |
| **Anahtar Uzunluğu** | 128-Bit |
| **Tur Sayısı** | 10 Tur (Rounds) |
| **Dil** | Python 3.x |

## 🧮 Algoritma Mimarisi

Bu algoritma, Claude Shannon'un **Karıştırma (Confusion)** ve **Yayılma (Diffusion)** ilkelerine dayanarak tasarlanmıştır.

### 1. İkame Katmanı (SubBytes) - *Karıştırma*
[cite_start]Bellek harcayan statik S-Box tabloları yerine, her byte ($b$) için aşağıdaki doğrusal olmayan (non-linear) fonksiyon kullanılır [cite: 26-29]:

$$S(b) = (b \times 5 + 13) \pmod{256}$$

### 2. Permütasyon Katmanı (ShiftRows) - *Yayılma*
[cite_start]16 Byte'lık veri bloğu 4x4 matris olarak işlenir ve satırlar sola kaydırılır [cite: 31-36]:
* **1. Satır:** Sabit (Kaydırma yok)
* **2. Satır:** 1 Byte Sola
* **3. Satır:** 2 Byte Sola
* **4. Satır:** 3 Byte Sola

### 3. Anahtar Genişletme (Key Schedule)
Ana anahtardan 10 adet farklı tur anahtarı üretilir. [cite_start]Her yeni anahtar, bir öncekinin **sola 3 bit kaydırılıp** (rotate) tur sayacı ile **XOR** lanmasıyla elde edilir [cite: 23-25].

---

## 🚀 Kurulum ve Çalıştırma

Bu projeyi çalıştırmak için bilgisayarınızda **Python 3** yüklü olmalıdır.

1. **Repoyu Klonlayın:**
   ```bash
   git clone [https://github.com/Osmanogutcu/GOLGE-128.git](https://github.com/Osmanogutcu/GOLGE-128.git)
   cd GOLGE-128
