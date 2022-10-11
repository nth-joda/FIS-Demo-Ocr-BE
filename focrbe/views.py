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
from PIL import Image, ImageFont, ImageDraw
from django.core.files.base import ContentFile
import base64
import time
import json
import cv2
import Levenshtein
import os
from io import BytesIO
import unidecode
import random
from.serializers import DetectionSerializer
# Create your views here.
# Setup PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')
# Setup VietOCR
config = Cfg.load_config_from_name('vgg_transformer')
# config['weights'] = './weights/transformerocr.pth'
config['weights'] = 'weights/vietOcr/transformerocr.pth'
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


def putTextTo(image, text, box, color):
    (r, g, b) = color
    fontSize = box[3] - box[1] - 2
    if(fontSize > 30):
        fontSize = fontSize - 15
    image = Image.fromarray(image)
    font = ImageFont.truetype("arial.ttf", int(fontSize))
    draw = ImageDraw.Draw(image)
    draw.rectangle([(box[0], box[1]), (box[2], box[3])],
                   outline=color, width=int(fontSize/10))
    draw.text((box[0], box[1]-fontSize), text, color, font=font)

    return np.array(image)


def det_VNese_Text(boxes, image_arr):
    detected_text = []
    text_image = image_arr
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

        r = random.randint(0, 88)
        g = random.randint(0, 88)
        b = random.randint(0, 88)
        text_image = putTextTo(
            text_image, dt, [top_left_x, top_left_y, bot_right_x, bot_right_y], (r, g, b))

    return detected_text, text_image


def ocr_detect(data, type):
    image = data['image']
    image = image.split(';base64,')[1]
    image = ContentFile(base64.b64decode(image), name='image.png')
    detectionObject = Detection(image=image, type=type, resultImage=image)
    save_model = detectionObject.save()
    filePath = save_model.image.path
    ''' orc distinguish  '''
    print("filePath is ", filePath)
    responseObj = {
        'message': 'successful!',
    }
    start_time = time.time()
    boxes, txts, scores = getBoxes_Texts_Scores(filePath)
    cmnd_img = cv2.imread(filePath)
    cmnd_text, text_image = det_VNese_Text(boxes, cmnd_img)
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

    if (type == "cmnd" or type == "all"):
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
        responseObj['cmnd'] = json.dumps(
            cmnd_detected.__dict__, indent=4, sort_keys=True)

    if(type == "donXinNghiViec" or type == "all"):
        donXinNghiViecModel = donXinNghiViecMapper(full_string)
        donXinNghiViecModel.save()
        responseObj['donXinNghiViec'] = json.dumps(
            model_to_dict(donXinNghiViecModel), indent=4, sort_keys=True)

    period = time.time() - start_time
    buffered = BytesIO()
    Image.fromarray(text_image).save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    responseObj['processedTime'] = period
    responseObj['rawText'] = full_string
    responseObj['textImage'] = img_str.decode('utf-8')

    return JsonResponse(responseObj, status=status.HTTP_200_OK)


class ImageDetection(ListCreateAPIView):
    model = Detection
    # ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def get_queryset(self):
        return Detection.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            type = data['type']
            return ocr_detect(data, type=type)

        except Exception as e:
            return JsonResponse({
                'message': str(e),
                'data': data
            }, status=status.HTTP_400_BAD_REQUEST)


def error(request, *args, **argv):
    return render(request, 'pages/error.html')
