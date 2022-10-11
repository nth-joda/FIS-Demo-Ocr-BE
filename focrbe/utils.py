import Levenshtein
import os
import unidecode

import re
from difflib import SequenceMatcher


from focrbe.models import DonXinNghiViec


def remove_accent(text):
    return unidecode.unidecode(text)


def getStringDifferent(string1, string2):
    string1 = string1.lower()
    string1 = remove_accent(string1)
    string2 = string2.lower()
    string2 = remove_accent(string2)
    maxLeng = max(len(string1), len(string2))
    return Levenshtein.distance(string1, string2) / maxLeng


def digital_sequence(s, sort_literal=False, fullwidth_digits=False):
    """Get sorted list of numbers.

    Args:
        s (str): arbitrary string
        sort_literal (bool): literal sort
        fullwidth_digits (bool): accept full-width digits

    Returns:
        list
    """
    r = r"\d+" if fullwidth_digits else r"[0-9]+"
    k = None if sort_literal else lambda x: int(x)
    return sorted(re.findall(r, s), key=k)


# def date_detection(s, sort_literal=False, fullwidth_digits=False):
#     """Get sorted list of numbers.

#     Args:
#         s (str): arbitrary string
#         sort_literal (bool): literal sort
#         fullwidth_digits (bool): accept full-width digits

#     Returns:
#         list
#     """
#     x = re.findall(
#         "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$", s)
#     return x
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class DonXinNghiViecUtils:

    def getTenCongty(text, mile):
        startLabel = "Giám đốc Công ty"
        endLabel = "Trưởng phòng nhân sự"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(endLabel.lower(), indexStartLabel +
                                              len(startLabel), int(len(text)))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getTenPhongNhanSu(text, mile):
        startLabel = "Trưởng phòng nhân sự"
        endLabel = "Trưởng phòng"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getTenTruongPhong(text, mile):
        startLabel = "Trưởng phòng"
        endLabel = "Tôi tên là"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getHoVaTen(text, mile):
        startLabel = "Tôi tên là"
        endLabel = "Ngày tháng năm sinh"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getNgaySinh(text, mile):
        startLabel = "Ngày tháng năm sinh"
        endLabel = "Chức vụ"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getChucVu(text, mile):
        startLabel = "Chức vụ"
        endLabel = "Bộ phận"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getBoPhan(text, mile):
        startLabel = "Bộ phận"
        endLabel = "Tôi làm đơn này"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getNgayNghi(text, mile):
        startLabel = "kể từ ngày"
        endLabel = "với lý do"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getLyDo(text, mile):
        startLabel = "với lý do"
        endLabel = "Tôi rất hài lòng"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getThoiGianGanBo(text, mile):
        startLabel = "gian qua. Hơn"
        endLabel = "làm việc"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getKinhNghiem(text, mile):
        startLabel = "nhiều kinh nghiệm"
        endLabel = "Tôi xin chân"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getNguoiBanGiao(text, mile):
        startLabel = "dụng cụ cho ông/bà"
        endLabel = "Bộ phận"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getBoPhanBanGiao(text, mile):
        startLabel = "Bộ phận"
        endLabel = "Các công việc được bàn giao"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getCongViecBanGiao(text, mile):
        startLabel = "Các công việc được bàn giao"
        endLabel = "Tôi cam đoan sẽ"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile

    def getNgayVietDon(text, mile):
        startLabel = "Xin trân trọng cảm ơn"
        endLabel = " Người làm đơn"
        result = ""
        try:
            indexStartLabel = text.lower().find(startLabel.lower(), mile, len(text))
            indexEndLabel = text.lower().find(
                endLabel.lower(), indexStartLabel+len(startLabel), len(text))
            if indexEndLabel > 0:
                mile = int(indexEndLabel)
            result = text[int(indexStartLabel) +
                          int(len(startLabel)): int(indexEndLabel)]
        except Exception as e:
            result = str(e)
        return result, mile


def donXinNghiViecMapper(raw_text):
    milestone = 0
    tenCongty, milestone = DonXinNghiViecUtils.getTenCongty(
        raw_text, milestone)
    tenPhongNhanSu, milestone = DonXinNghiViecUtils.getTenPhongNhanSu(
        raw_text, milestone)
    tenTruongPhong, milestone = DonXinNghiViecUtils.getTenTruongPhong(
        raw_text, milestone)
    hoVaTen, milestone = DonXinNghiViecUtils.getHoVaTen(raw_text, milestone)
    ngaySinh, milestone = DonXinNghiViecUtils.getNgaySinh(raw_text, milestone)
    chucVu,  milestone = DonXinNghiViecUtils.getChucVu(raw_text, milestone)
    boPhan, milestone = DonXinNghiViecUtils.getBoPhan(raw_text, milestone)
    ngayNghi, milestone = DonXinNghiViecUtils.getNgayNghi(raw_text, milestone)
    lyDo,  milestone = DonXinNghiViecUtils.getLyDo(raw_text, milestone)
    thoiGianGanBo,  milestone = DonXinNghiViecUtils.getThoiGianGanBo(
        raw_text, milestone)
    kinhNghiem,  milestone = DonXinNghiViecUtils.getKinhNghiem(
        raw_text, milestone)
    nguoiBanGiao,  milestone = DonXinNghiViecUtils.getNguoiBanGiao(
        raw_text, milestone)
    boPhanBanGiao, milestone = DonXinNghiViecUtils.getBoPhanBanGiao(
        raw_text, milestone)
    congViecBanGiao,  milestone = DonXinNghiViecUtils.getCongViecBanGiao(
        raw_text, milestone)
    ngayVietDon, milestone = DonXinNghiViecUtils.getNgayVietDon(
        raw_text, milestone)
    specialCharacter = "[$@&?:]+"
    return DonXinNghiViec(
        tenCongTy=re.sub(specialCharacter, '', tenCongty),
        tenPhongNhanSu=re.sub(specialCharacter, '', tenPhongNhanSu),
        tenTruongPhong=re.sub(specialCharacter, '', tenTruongPhong),
        hoVaTen=re.sub(specialCharacter, '', hoVaTen),
        ngaySinh=re.sub(specialCharacter, '-', ngaySinh),
        chucVu=re.sub(specialCharacter, '', chucVu),
        boPhan=re.sub(specialCharacter, '', boPhan),
        nghiTuNgay=re.sub(specialCharacter, '-', ngayNghi),
        lyDo=re.sub(specialCharacter, '', lyDo),
        thoiGianGanBo=re.sub(specialCharacter, '', thoiGianGanBo),
        kinhNghiem=re.sub(specialCharacter, '', kinhNghiem),
        nguoiBanGiao=re.sub(specialCharacter, ' ', nguoiBanGiao),
        boPhanBanGiao=re.sub(specialCharacter, ' ', boPhanBanGiao),
        congViecBanGiao=re.sub(specialCharacter, '_', congViecBanGiao),
        ngayVietDon=re.sub(specialCharacter, '', ngayVietDon)
    )
