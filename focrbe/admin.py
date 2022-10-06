from django.contrib import admin
from .models import Detection, ChungMinhNhanDan, DonXinNghiViec
# Register your models here.


class DetectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'type', 'result', 'created', 'updated')
    list_filter = ('id', 'type', 'result', 'created', 'updated')
    search_fields = ('type', 'result', 'created', 'updated')
    date_hierarchy = 'created'
    ordering = ('-created',)
    readonly_fields = ['created', 'updated']
    fieldsets = (
        (None, {
            'fields': ('image', 'type', 'result')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created', 'updated')
        }),
    )


class ChungMinhNhanDanAdmin(admin.ModelAdmin):
    list_display = ('id', 'soCmnd', 'hoVaTen',
                    'ngaySinh', 'nguyenQuan', 'noiDktt')
    list_filter = ('id', 'soCmnd', 'hoVaTen',
                   'ngaySinh', 'nguyenQuan', 'noiDktt')
    search_fields = ('soCmnd', 'hoVaTen', 'ngaySinh', 'nguyenQuan', 'noiDktt')
    ordering = ('-id',)
    readonly_fields = ['id']
    fieldsets = (
        (None, {
            'fields': ('soCmnd', 'hoVaTen', 'ngaySinh', 'nguyenQuan', 'noiDktt')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id',)
        }),
    )

class DonXinNghiViecAdmin(admin.ModelAdmin):

    list_display = ('tenCongTy', 'tenPhongNhanSu', 'tenTruongPhong',
                    'hoVaTen', 'ngaySinh', 'chucVu', 'boPhan', 'nghiTuNgay', 'lyDo',
                    'thoiGianGanBo', 'kinhNghiem', 'nguoiBanGiao', 'boPhanBanGiao',
                    'congViecBanGiao', 'ngayVietDon')
    list_filter = ('tenCongTy', 'tenPhongNhanSu', 'tenTruongPhong',
                   'hoVaTen', 'ngaySinh', 'chucVu', 'boPhan', 'nghiTuNgay',
                   'lyDo', 'thoiGianGanBo', 'kinhNghiem', 'nguoiBanGiao',
                   'boPhanBanGiao', 'congViecBanGiao', 'ngayVietDon')
    search_fields = ('hoVaTen', 'ngaySinh', 'chucVu', 'boPhan', 'nguoiBanGiao', 'boPhanBanGiao')
    ordering = ('-id',)
    readonly_fields = ['id']
    fieldsets = (
        (None, {
            'fields': ('tenCongTy', 'tenPhongNhanSu', 'tenTruongPhong',
                   'hoVaTen', 'ngaySinh', 'chucVu', 'boPhan', 'nghiTuNgay',
                   'lyDo', 'thoiGianGanBo', 'kinhNghiem', 'nguoiBanGiao',
                   'boPhanBanGiao', 'congViecBanGiao', 'ngayVietDon')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id',)
        }),
    )


admin.site.register(Detection, DetectionAdmin)
admin.site.register(ChungMinhNhanDan, ChungMinhNhanDanAdmin)
admin.site.register(DonXinNghiViec, DonXinNghiViecAdmin)
