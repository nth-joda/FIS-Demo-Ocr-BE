from django.db import models

# Create your models here.


class Detection(models.Model):
    image = models.ImageField(upload_to='images/')
    type = models.TextField()
    result = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

    def save(self):
        super().save()
        return self


class ChungMinhNhanDan(models.Model):
    soCmnd = models.TextField()
    hoVaTen = models.TextField()
    ngaySinh = models.TextField()
    nguyenQuan = models.TextField()
    noiDktt = models.TextField()
    imagePath = models.TextField(default="")

    def __str__(self):
        return self.soCmnd + " - " + self.hoVaTen
    

class DonXinNghiViec(models.Model):
    tenCongTy = models.TextField()
    tenPhongNhanSu = models.TextField()
    tenTruongPhong = models.TextField()
    hoVaTen = models.TextField()
    ngaySinh = models.TextField()
    chucVu = models.TextField()
    boPhan = models.TextField()
    nghiTuNgay = models.TextField()
    lyDo = models.TextField()
    thoiGianGanBo = models.TextField()
    kinhNghiem =models.TextField()
    nguoiBanGiao = models.TextField()
    boPhanBanGiao = models.TextField()
    congViecBanGiao = models.TextField()
    ngayVietDon = models.TextField()
    def __str__(self):
        return self.hoVaTen + " - " + self.chucVu + " - " + self.boPhan
