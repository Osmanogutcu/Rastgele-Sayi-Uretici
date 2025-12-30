# Rastgele-Sayi-Uretici
Hazır kütüphaneler kullanmadan sözde rastgele sayı üretim mantığını göstermek için C# ile yazılmış özel bir LCG algoritması uygulaması
# GÖLGE-128 (Shadow-128) Şifreleme Algoritması

[cite_start]Bu proje, **GÖLGE-128 (Shadow-128)** adı verilen özel tasarım bir blok şifreleme algoritmasının C# dili ile gerçekleştirilmiş referans uygulamasıdır[cite: 3].

[cite_start]Algoritma, **SPN (Substitution-Permutation Network)** mimarisi üzerine kuruludur ve hız ile güvenlik dengesi gözetilerek tasarlanmıştır[cite: 5].

## 📋 Proje Hakkında
[cite_start]Bu çalışma, kriptografik tasarım prensipleri olan **Karıştırma (Confusion)** ve **Yayılma (Diffusion)** ilkelerinin yazılım tabanlı simülasyonunu amaçlar[cite: 9, 11]. [cite_start]Standart AES yapısına benzemekle birlikte, işlemci gücünü verimli kullanmak adına S-Box tabloları yerine matematiksel fonksiyonlar kullanılmıştır[cite: 28].

## ⚙️ Teknik Özellikler
* [cite_start]**Blok Boyutu:** 128-bit (16 Byte) [cite: 17]
* [cite_start]**Anahtar Boyutu:** 128-bit [cite: 13]
* [cite_start]**Tur Sayısı (Rounds):** 10 Tur [cite: 15]
* [cite_start]**Mimari:** SPN (Substitution Permutation Network) [cite: 5]
* **Dil:** C# (.NET Core / Framework)

## 🧮 Algoritma Mantığı
[cite_start]GÖLGE-128, her turda aşağıdaki 3 temel katmanı uygular [cite: 38-44]:

### 1. Anahtar Karıştırma (AddRoundKey)
[cite_start]Veri bloğu, o tur için üretilen tur anahtarı (Round Key) ile XOR işlemine tabi tutulur[cite: 42].

### 2. İkame Katmanı (SubBytes - Non-Linear)
[cite_start]Klasik bellek tabanlı S-Box yerine, her byte ($b$) için aşağıdaki doğrusal olmayan matematiksel dönüşüm uygulanır[cite: 29]:

$$S(b) = (b \times 5 + 13) \mod 256$$

[cite_start]Bu işlem sistemin **Karıştırma (Confusion)** özelliğini sağlar[cite: 30].

### 3. Permütasyon Katmanı (ShiftRows - Linear)
[cite_start]16 byte'lık veri 4x4 matris olarak düşünülür ve satırlar sola kaydırılır[cite: 32]:
* **1. [cite_start]Satır:** Sabit [cite: 33]
* **2. [cite_start]Satır:** 1 Byte sola [cite: 34]
* **3. [cite_start]Satır:** 2 Byte sola [cite: 35]
* **4. [cite_start]Satır:** 3 Byte sola [cite: 36]

[cite_start]Bu işlem sistemin **Yayılma (Diffusion)** özelliğini sağlar[cite: 37].

## 🚀 Kurulum ve Çalıştırma

1. Projeyi klonlayın veya indirin.
2. `.sln` dosyasını **Visual Studio** ile açın.
3. `Program.cs` dosyasını derleyin ve çalıştırın.
4. Konsol ekranında şifrelenmiş metnin Hex çıktısını görebilirsiniz.

## ⚠️ Yasal Uyarı
Bu proje **eğitim ve akademik araştırma** amacıyla geliştirilmiştir. Kriptografik olarak askeri veya ticari düzeyde güvenlik garantisi vermez. Gerçek dünyadaki hassas verilerin korunması için AES gibi standart algoritmalar kullanılmalıdır.

---
*Geliştirici: [Osman Kerim Ögütçü]*
