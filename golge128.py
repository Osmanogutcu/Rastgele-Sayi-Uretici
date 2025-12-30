import struct

# --- GÖLGE-128 (Shadow-128) Şifreleme Algoritması ---
# Proje: Kriptografik Algoritma Geliştirme ve Analizi
# Geliştirici: [Adını Buraya Yazabilirsin]

# --- SABİTLER ---
# Deşifreleme için çarpımsal ters: 5 * 205 = 1025 = 1 (mod 256)
INV_MULT = 205 

def anahtar_uret(parola):
    """
    Kullanıcı parolasını 128-bit (16 byte) anahtara tamamlar.
    """
    parola_bytes = parola.encode('utf-8')
    if len(parola_bytes) < 16:
        # Eksikse sonuna 0 ekle (Padding)
        return parola_bytes + b'\x00' * (16 - len(parola_bytes))
    return parola_bytes[:16] # Fazlaysa kes

def anahtar_genislet(ana_anahtar):
    """
    10 Tur anahtarı üretir. (Rotate + XOR mantığı)
    """
    anahtarlar = []
    su_anki = int.from_bytes(ana_anahtar, byteorder='big')

    for i in range(10):
        # Sola 3 bit dairesel kaydır (Rotate Left)
        su_anki = ((su_anki << 3) | (su_anki >> (128 - 3))) & ((1 << 128) - 1)
        
        yeni_anahtar = bytearray(su_anki.to_bytes(16, byteorder='big'))
        # Tur sayısını XOR'la (Karıştırma)
        for j in range(16):
            yeni_anahtar[j] ^= (i + 1)
        
        anahtarlar.append(yeni_anahtar)
        su_anki = int.from_bytes(yeni_anahtar, byteorder='big')
    return anahtarlar

# --- ŞİFRELEME ---
def sifrele(duz_metin, anahtar):
    # Metni 16 byte katlarına tamamla
    while len(duz_metin) % 16 != 0:
        duz_metin += b'\x00'
    
    state = bytearray(duz_metin)
    tur_anahtarlari = anahtar_genislet(anahtar)

    for i in range(10):
        # 1. AddRoundKey
        for j in range(16): state[j] ^= tur_anahtarlari[i][j]
        
        # 2. SubBytes: (x * 5 + 13) % 256
        for j in range(16): state[j] = (state[j] * 5 + 13) % 256
        
        # 3. ShiftRows (Satır Kaydırma)
        s = state[:]
        state[4:8]   = s[5:8]   + s[4:5]   # 1 Sola
        state[8:12]  = s[10:12] + s[8:10]  # 2 Sola
        state[12:16] = s[15:16] + s[12:15] # 3 Sola

    return bytes(state)

# --- DEŞİFRELEME ---
def desifrele(sifreli_metin, anahtar):
    state = bytearray(sifreli_metin)
    tur_anahtarlari = anahtar_genislet(anahtar)

    # İşlemleri tersten yap (Tur 9'dan 0'a)
    for i in range(9, -1, -1):
        # 1. Inverse ShiftRows (Sağa Kaydır)
        s = state[:]
        state[4:8]   = s[7:8]   + s[4:7]   # 1 Sağa
        state[8:12]  = s[10:12] + s[8:10]  # 2 Sağa
        state[12:16] = s[13:16] + s[12:13] # 3 Sağa

        # 2. Inverse SubBytes: (y - 13) * 205 % 256
        for j in range(16):
            val = (state[j] - 13) % 256
            state[j] = (val * INV_MULT) % 256

        # 3. Inverse AddRoundKey
        for j in range(16): state[j] ^= tur_anahtarlari[i][j]

    return bytes(state).rstrip(b'\x00')

# --- TEST VE MEYDAN OKUMA ---
if __name__ == "__main__":
    print("--- GÖLGE-128 TESTLERİ ÇALIŞIYOR ---")
    
    # TEST 1: Doğrulama
    p = "GizliAnahtar"
    m = b"DenemeMesaji123"
    enc = sifrele(m, anahtar_uret(p))
    dec = desifrele(enc, anahtar_uret(p))
    print(f"[TEST 1] Şifreleme/Çözme: {'✅ BAŞARILI' if m in dec else '❌ HATALI'}")

    # TEST 2: Çığ Etkisi
    k1 = anahtar_uret("A")
    k2 = anahtar_uret("B") # Tek bit fark
    c1 = sifrele(b"TestVerisi123456", k1)
    c2 = sifrele(b"TestVerisi123456", k2)
    fark = sum(1 for a, b in zip(c1, c2) if a != b)
    print(f"[TEST 2] Çığ Etkisi (Değişen Byte): {fark}/16 {'✅ İYİ' if fark > 8 else '⚠️ ZAYIF'}")

    # --- README İÇİN CHALLENGE OLUŞTURUCU ---
    # Hocanın veya arkadaşının kırması gereken şifreyi burada üretiyoruz.
    # Şifre: "2024" (Sadece 4 rakam seçtik ki Brute-Force ile kırılabilsin)
    
    challenge_key = anahtar_uret("2024")
    challenge_msg = b"TebriklerKirdin!"
    challenge_cipher = sifrele(challenge_msg, challenge_key)
    
    print("\n--- README DOSYASINA YAPIŞTIRILACAK HEX KODU ---")
    print(f"Bunu kopyala: {challenge_cipher.hex().upper()}")
    print("Gerçek Şifre (Kimseye söyleme): 2024")