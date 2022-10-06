from unittest import result

from django.forms import model_to_dict
from focrbe.utils import donXinNghiViecMapper
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
from http.client import HTTPResponse
from urllib import response
from django.shortcuts import render
from django.http import JsonResponse
from focrbe.models import ChungMinhNhanDan, Detection
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from PaddleOCR.paddleocr import PaddleOCR, draw_ocr
import numpy as np
from PIL import Image
from django.core.files.base import ContentFile
import base64
import time

import json
import cv2
import Levenshtein
import os
import unidecode
from.serializers import DetectionSerializer
# Create your views here.
# Setup PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')
# Setup VietOCR
config = Cfg.load_config_from_name('vgg_transformer')
# config['weights'] = './weights/transformerocr.pth'
config['weights'] = 'PaddleOCR/pretrained/transformerocr.pth'
config['cnn']['pretrained'] = False
# config['device'] = 'cuda:0'
config['device'] = 'cpu'
config['predictor']['beamsearch'] = False
detector = Predictor(config)


def remove_accent(text):
    return unidecode.unidecode(text)


def getStringDifferent(string1, string2):
    string1 = string1.lower()
    string1 = remove_accent(string1)
    string2 = string2.lower()
    string2 = remove_accent(string2)
    maxLeng = max(len(string1), len(string2))
    return Levenshtein.distance(string1, string2) / maxLeng


def index(request):
    response = HTTPResponse()
    response.write(b'Hello World')
    return response


def getBoxes_Texts_Scores(img_path):
    result = ocr.ocr(img_path, cls=True)
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    return boxes, txts, scores


class Cmnd:
    def __init__(self, fields):
        self.soCmnd = fields[0]
        self.hoTen = fields[1]
        self.ngaySinh = fields[2]
        self.nguyenQuan = fields[3]
        self.noiDktt = fields[4]


# Các fields cần nhận dạng:
soCmnd = ["SỐ", "Họ tên", "", -1, -1, "Số chứng minh nhân dân"]
hoTen = ["Họ tên", "Sinh ngày", "", -1, -1, "Họ tên"]
ngaySinh = ["Sinh ngày", "Nguyên quán", "", -1, -1, "Ngày sinh"]
nguyenQuan = ["Nguyên quán", "Nơi ĐKHK thường trú", "", -1, -1, "Nguyên quán"]
noiDkhkTt = ["Nơi ĐKHK thường trú", "end",
             "", -1, -1, "Nơi đăng ký hộ khẩu thường trú"]
cmnd_fields = [soCmnd, hoTen, ngaySinh, nguyenQuan, noiDkhkTt]


def det_VNese_Text(boxes, image_arr):
    detected_text = []
    for i in range(len(boxes)):
        box = boxes[i]
        box = np.reshape(np.array(box), [-1, 1, 2]).astype(np.int64)
        top_left_x = min([box[0][0][0], box[1][0][0],
                         box[2][0][0], box[3][0][0]])
        top_left_y = min([box[0][0][1], box[1][0][1],
                         box[2][0][1], box[3][0][1]])
        bot_right_x = max([box[0][0][0], box[1][0][0],
                          box[2][0][0], box[3][0][0]])
        bot_right_y = max([box[0][0][1], box[1][0][1],
                          box[2][0][1], box[3][0][1]])
        cropped_arr = np.array(
            image_arr[top_left_y:bot_right_y+1, top_left_x:bot_right_x+1])
        dt = detector.predict(Image.fromarray(cropped_arr))
        item = [[top_left_x, top_left_y, bot_right_x, bot_right_y], dt]
        detected_text.append(item)
    return detected_text


def ocr_detect(filePath):
    ''' orc distinguish  '''
    print("filePath is ", filePath)
    start_time = time.time()
    boxes, txts, scores = getBoxes_Texts_Scores(filePath)
    cmnd_img = cv2.imread(filePath)
    cmnd_text = det_VNese_Text(boxes, cmnd_img)
    full_string = ""
    for txtBlock in cmnd_text:
        full_string = full_string + txtBlock[1] + " "
    for field in cmnd_fields:
        blockSize = len(field[0])+1
        minDiff = 1
        stopPoint = -1
        startPoint = 0
        for stepSize in range(blockSize):
            for chaId in range(len(full_string) - stepSize):
                curDiff = getStringDifferent(
                    field[0], full_string[chaId: chaId+stepSize])
                if(curDiff < minDiff):
                    minDiff = curDiff
                    stopPoint = chaId + stepSize
                    if(len(field[0]) >= stepSize):
                        startPoint = chaId
        field[4] = stopPoint
        field[3] = startPoint

    # Lấy field values:
    for id in range(len(cmnd_fields)):
        field = cmnd_fields[id]
        if id < len(cmnd_fields) - 1:
            nextField = cmnd_fields[id + 1]
            print(nextField[3])
            field[2] = full_string[field[4]+1: nextField[3] - 1]
        else:
            field[2] = full_string[field[4]+1: len(full_string) - 1]
    cmndFields = []
    for field in cmnd_fields:
        cmndFields.append(field[2])
    cmnd_detected = Cmnd(cmndFields)

    model = ChungMinhNhanDan(soCmnd=cmnd_detected.soCmnd, hoVaTen=cmnd_detected.hoTen,
                             ngaySinh=cmnd_detected.ngaySinh, nguyenQuan=cmnd_detected.nguyenQuan, noiDktt=cmnd_detected.noiDktt, imagePath=filePath)
    model.save()
    donXinNghiViecModel = donXinNghiViecMapper(full_string)
    donXinNghiViecModel.save()
    cmnd_detected_json = json.dumps(cmnd_detected.__dict__, indent=4, sort_keys=True)
    donXinNghiViec_json = json.dumps(model_to_dict(donXinNghiViecModel), indent=4, sort_keys=True)
    period = time.time() - start_time
    return JsonResponse({
        'message': 'successful!', "rawText": full_string, "cmnd": cmnd_detected_json, "donXinNghiViec": donXinNghiViec_json, "processedTime": period
    }, status=status.HTTP_200_OK)


class ImageDetection(ListCreateAPIView):
    model = Detection
    # ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def get_queryset(self):
        return Detection.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            type = data['type']
            image = data['image']
            image = image.split(';base64,')[1]
            image = ContentFile(base64.b64decode(image), name='image.png')
            detectionObject = Detection(image=image, type=type)
            save_model = detectionObject.save()
            print(save_model)
            return ocr_detect(save_model.image.path)

        except Exception as e:
            return JsonResponse({
                'message': str(e),
                'data': data
            }, status=status.HTTP_400_BAD_REQUEST)


def error(request, *args, **argv):
    return render(request, 'pages/error.html')
