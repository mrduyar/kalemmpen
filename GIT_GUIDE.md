# 🚀 Kalemm Pen Pro - Git Gönderim Kılavuzu

Bu proje Git ile takip edilmek üzere hazırlandı. Kodlarınızı GitHub veya GitLab gibi bir platforma göndermek için aşağıdaki adımları izleyebilirsiniz.

## 1. Yeni Bir Depo (Repository) Oluşturun
GitHub veya GitLab hesabınızda `Kalemm` adında yeni bir boş depo oluşturun.

## 2. Yerel Depoyu Uzak Depoya Bağlayın
Aşağıdaki komutları terminalinize sırayla kopyalayıp yapıştırın (LINK kısmına kendi depo bağlantınızı yazın):

```bash
# Uzak depoyu ekle
git remote add origin https://github.com/KULLANICI_ADINIZ/Kalemm.git

# Ana dalı (branch) belirle
git branch -M main

# Kodları gönder
git push -u origin main
```

## 3. Güncelleme Yapmak İstediğinizde
Kodlarda değişiklik yaptıktan sonra şu 3 komutu kullanmanız yeterlidir:

```bash
git add .
git commit -m "Buraya yaptığınız değişikliği yazın"
git push
```

## 4. Dosya Yapısı Notları
- `.gitignore`: Sanal ortam (`.venv`), cache dosyaları ve ayar dosyalarının (`kalemm_config.json`) git'e gitmesini engeller.
- `requirements.txt`: Projenin çalışması için gerekli kütüphanelerin listesidir.

---
**Mutlu Kodlamalar!** ✒️🌲
