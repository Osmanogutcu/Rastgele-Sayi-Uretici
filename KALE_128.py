import struct

# --- KALE-128 (Castle-128) Şifreleme Algoritması ---
# Proje: Kriptografik Algoritma Geliştirme ve Analizi
# Mimari: SPN (Substitution-Permutation Network)
# Geliştirici: [Adını Buraya Yazabilirsin]

# --- SABİTLER ---
# Deşifreleme için çarpımsal ters: 5 * 205 = 1025 = 1 (mod 256)
# Bu, (x * 5 + 13) işleminin tersini almak için gereklidir.
INV_MULT = 205 

def anahtar_uret(parola):
    """
    Kullanıcı parolasını 128-bit (16 byte) anahtara tamamlar.
    Eksikse 'padding' ekler, fazlaysa kırpar.
    """
    parola_bytes = parola.encode('utf-8')
    if len(parola_bytes) < 16:
        # Eksikse sonuna 0 (null byte) ekle
        return parola_bytes + b'\x00' * (16 - len(parola_bytes))
    return parola_bytes[:16] # Fazlaysa ilk 16 karakteri al

def anahtar_genislet(ana_anahtar):
    """
    Ana anahtardan 10 adet Tur Anahtarı (Round Key) üretir.
    Yöntem: Bit Kaydırma (Rotate) + XOR Sabiti
    """
    anahtarlar = []
    su_anki = int.from_bytes(ana_anahtar, byteorder='big')

    for i in range(10):
        # 1. Sola 3 bit dairesel kaydır (Rotate Left)
        su_anki = ((su_anki << 3) | (su_anki >> (128 - 3))) & ((1 << 128) - 1)
        
        yeni_anahtar = bytearray(su_anki.to_bytes(16, byteorder='big'))
        
        # 2. Tur sayısını XOR'la (Karıştırma)
        for j in range(16):
            yeni_anahtar[j] ^= (i + 1)
        
        anahtarlar.append(yeni_anahtar)
        # Bir sonraki tur için tamsayı halini güncelle
        su_anki = int.from_bytes(yeni_anahtar, byteorder='big')
        
    return anahtarlar

# --- ŞİFRELEME (Encryption) ---
def sifrele(duz_metin, anahtar):
    """
    SPN Mimarisine göre şifreleme yapar.
    Aşamalar: AddRoundKey -> SubBytes -> ShiftRows
    """
    # Metni 16 byte katlarına tamamla (Padding)
    while len(duz_metin) % 16 != 0:
        duz_metin += b'\x00'
    
    state = bytearray(duz_metin)
    tur_anahtarlari = anahtar_genislet(anahtar)

    # 10 Tur (Rounds)
    for i in range(10):
        # 1. Anahtar Karıştırma (AddRoundKey)
        for j in range(16): state[j] ^= tur_anahtarlari[i][j]
        
        # 2. İkame Katmanı (SubBytes) - Matematiksel S-Box
        # Formül: (x * 5 + 13) % 256
        for j in range(16): state[j] = (state[j] * 5 + 13) % 256
        
        # 3. Permütasyon Katmanı (ShiftRows) - Satır Kaydırma
        # Veriyi 4x4 matris gibi düşün:
        s = state[:] # Kopyasını al
        # 1. Satır: Sabit
        state[4:8]   = s[5:8]   + s[4:5]   # 2. Satır: 1 Sola
        state[8:12]  = s[10:12] + s[8:10]  # 3. Satır: 2 Sola
        state[12:16] = s[15:16] + s[12:15] # 4. Satır: 3 Sola

    return bytes(state)

# --- DEŞİFRELEME (Decryption) ---
def desifrele(sifreli_metin, anahtar):
    """
    Şifreleme işlemlerinin tam tersini ters sırayla uygular.
    """
    state = bytearray(sifreli_metin)
    tur_anahtarlari = anahtar_genislet(anahtar)

    # İşlemleri tersten yap (Tur 9'dan 0'a)
    for i in range(9, -1, -1):
        # 1. Ters Permütasyon (Inverse ShiftRows) - Sağa Kaydır
        s = state[:]
        state[4:8]   = s[7:8]   + s[4:7]   # 1 Sağa
        state[8:12]  = s[10:12] + s[8:10]  # 2 Sağa
        state[12:16] = s[13:16] + s[12:13] # 3 Sağa

        # 2. Ters İkame (Inverse SubBytes)
        # Matematiksel tersi: (y - 13) * 205 % 256
        for j in range(16):
            val = (state[j] - 13) % 256
            state[j] = (val * INV_MULT) % 256

        # 3. Ters Anahtar Karıştırma (Inverse AddRoundKey)
        for j in range(16): state[j] ^= tur_anahtarlari[i][j]

    # Eklenen boşlukları (padding) temizle
    return bytes(state).rstrip(b'\x00')

# --- TEST VE MEYDAN OKUMA ---
if __name__ == "__main__":
    print("--- KALE-128 (Castle-128) TESTLERİ BAŞLATILIYOR ---")
    
    # TEST 1: Doğrulama (Verification)
    # Şifrelenen metin geri açılabiliyor mu?
    p_test = "GizliAnahtar"
    m_test = b"KriptoOdevTesti"
    enc = sifrele(m_test, anahtar_uret(p_test))
    dec = desifrele(enc, anahtar_uret(p_test))
    
    print(f"\n[TEST 1] Şifreleme/Çözme Doğrulaması:")
    print(f"  Durum: {'✅ BAŞARILI' if m_test in dec else '❌ HATALI'}")
    print(f"  Metin: {dec.decode('utf-8', errors='ignore')}")

    # TEST 2: Çığ Etkisi (Avalanche Effect)
    # Anahtardaki 1 bitlik değişim sonucu ne kadar değiştiriyor?
    k1 = anahtar_uret("A")
    k2 = anahtar_uret("B") # 'A' ve 'B' arasında sadece 1-2 bit fark vardır.
    c1 = sifrele(b"TestVerisi123456", k1)
    c2 = sifrele(b"TestVerisi123456", k2)
    
    fark_byte = sum(1 for a, b in zip(c1, c2) if a != b)
    print(f"\n[TEST 2] Anahtar Hassasiyeti (Çığ Etkisi):")
    print(f"  Değişen Byte: {fark_byte}/16")
    print(f"  Sonuç: {'✅ İYİ (Güvenli)' if fark_byte > 8 else '⚠️ ZAYIF'}")

    # --- README İÇİN CHALLENGE (MEYDAN OKUMA) ---
    # Hocanın veya arkadaşının kırması gereken şifreyi burada üretiyoruz.
    # Şifre olarak "2024" (4 rakam) seçtik ki Brute-Force ile kırılabilsin.
    
    print(f"\n--- [KALE-128] MEYDAN OKUMA VERİSİ ---")
    challenge_key = anahtar_uret("2024") # Kırılması gereken şifre
    challenge_msg = b"TebriklerKirdin!"
    challenge_cipher = sifrele(challenge_msg, challenge_key)
    
    print(f"README dosyasına yapıştırılacak HEX kodu:")
    print(f"{challenge_cipher.hex().upper()}")
    print("(Not: Bu kodun şifresi '2024'tür, kimseye söyleme!)")