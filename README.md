# DJANGO

## 1. Các lệnh cơ bản

---

- Tạo project: `django-admin startproject <project_name>`
- Khởi chạy project: `python manage.py runserver` trong 1 environment cmd:

```apache
(focrDjSep22) D:\Documents\PK's_Workplace\__FIS__\Backend\__FOcr__\__Open_Sources__\__Django__\djFisOcr>python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

[2022/09/18 13:52:12] ppocr DEBUG: Namespace(help='==SUPPRESS==', use_gpu=False, use_xpu=False, ir_optim=True, use_tensorrt=False, min_subgraph_size=15, shape_info_filename=None, precision='fp32', gpu_mem=500, image_dir=None, det_algorithm='DB', det_model_dir='C:\\Users\\ASUS/.paddleocr/whl\\det\\en\\en_PP-OCRv3_det_infer', det_limit_side_len=960, det_limit_type='max', det_db_thresh=0.3, det_db_box_thresh=0.6, det_db_unclip_ratio=1.5, max_batch_size=10, use_dilation=False, det_db_score_mode='fast', det_east_score_thresh=0.8, det_east_cover_thresh=0.1, det_east_nms_thresh=0.2, det_sast_score_thresh=0.5, det_sast_nms_thresh=0.2, det_sast_polygon=False, det_pse_thresh=0, det_pse_box_thresh=0.85, det_pse_min_area=16, det_pse_box_type='quad', det_pse_scale=1, scales=[8, 16, 32], alpha=1.0, beta=1.0, fourier_degree=5, det_fce_box_type='poly', rec_algorithm='SVTR_LCNet', rec_model_dir='C:\\Users\\ASUS/.paddleocr/whl\\rec\\en\\en_PP-OCRv3_rec_infer', rec_image_shape='3, 48, 320', rec_batch_num=6, max_text_length=25, rec_char_dict_path="D:\\Documents\\PK's_Workplace\\__FIS__\\Backend\\__FOcr__\\__Open_Sources__\\__Django__\\djFisOcr\\PaddleOCR\\ppocr\\utils\\en_dict.txt", use_space_char=True, vis_font_path='./doc/fonts/simfang.ttf', drop_score=0.5, e2e_algorithm='PGNet', e2e_model_dir=None, e2e_limit_side_len=768, e2e_limit_type='max', e2e_pgnet_score_thresh=0.5, e2e_char_dict_path='./ppocr/utils/ic15_dict.txt', e2e_pgnet_valid_set='totaltext', e2e_pgnet_mode='fast', use_angle_cls=True, cls_model_dir='C:\\Users\\ASUS/.paddleocr/whl\\cls\\ch_ppocr_mobile_v2.0_cls_infer', cls_image_shape='3, 48, 192', label_list=['0', '180'], cls_batch_num=6, cls_thresh=0.9, enable_mkldnn=False, cpu_threads=10, use_pdserving=False, warmup=False, sr_model_dir=None, sr_image_shape='3, 32, 128', sr_batch_num=1, draw_img_save_dir='./inference_results', save_crop_res=False, crop_res_save_dir='./output', use_mp=False, total_process_num=1, process_id=0, benchmark=False, save_log_path='./log_output/', show_log=True, use_onnx=False, output='./output', table_max_len=488, table_algorithm='TableAttn', table_model_dir=None, merge_no_span_structure=True, table_char_dict_path=None, layout_model_dir=None, layout_dict_path=None, layout_score_threshold=0.5, layout_nms_threshold=0.5, kie_algorithm='LayoutXLM', ser_model_dir=None, ser_dict_path='../train_data/XFUND/class_list_xfun.txt', ocr_order_method=None, mode='structure', image_orientation=False, layout=True, table=True, ocr=True, recovery=False, save_pdf=False, lang='en', det=True, rec=True, type='ocr', ocr_version='PP-OCRv3', structure_version='PP-Structurev2')
System check identified no issues (0 silenced).
September 18, 2022 - 13:52:15
Django version 4.1, using settings 'djFisOcr.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

```

- Khởi tạo 1 application: `python manage.py startapp <app_name>`; ví dụ app `focrbe`:

```apache
FOCRBE
│   admin.py --> Đăng ký models cho admin quản lý
│   apps.py --> Định nghĩa tên application
│   models.py --> Giống như entities trong spring
│   serializers.py
│   tests.py
│   urls.py --> Controller điều hướng các url
│   utils.py
│   views.py
│   __init__.py --> Đánh dấu folder này là 1 module của python
│
├───migrations --> Lịch sử tạo/xóa/sửa database
│   │   0001_initial.py
│   │   0002_rename_dectection_detection.py
│   │   0003_chungminhnhandan.py
│   │   0004_rename_gioitinh_chungminhnhandan_nguyenquan_and_more.py
│   │   0005_chungminhnhandan_imagepath.py
│   │   __init__.py
│   │
│   └───__pycache__
│           0001_initial.cpython-310.pyc
│           0002_rename_dectection_detection.cpython-310.pyc
│           0003_chungminhnhandan.cpython-310.pyc
│           0004_rename_gioitinh_chungminhnhandan_nguyenquan_and_more.cpython-310.pyc
│           0005_chungminhnhandan_imagepath.cpython-310.pyc
│           __init__.cpython-310.pyc
│
├───templates
│   └───pages
│           error.html
│
└───__pycache__
        admin.cpython-310.pyc
        apps.cpython-310.pyc
        models.cpython-310.pyc
        serializers.cpython-310.pyc
        urls.cpython-310.pyc
        utils.cpython-310.pyc
        views.cpython-310.pyc
        __init__.cpython-310.pyc
```

- `python manage.py makemigrations` cập nhật các thay đổi của models vào migrations
- `python manage.py migrate` áp dụng migrations
- `python manage.py shell` mở termial của python

## 2. Cấu trúc thư mục:

```apache
DjFisOcr
├───djFisOcr
│    │   asgi.py
│    │   settings.py --> đăng ký các app của project, database, static folder/file
│    │   urls.py --> Controller điều hướng các url
│    │   wsgi.py
│    │   __init__.py
│    │
│    └───__pycache__
│            settings.cpython-310.pyc
│            urls.cpython-310.pyc
│            wsgi.cpython-310.pyc
│            __init__.cpython-310.pyc
├───focrbe --> application
├───gcloud
├───media
│   └───images
├───PaddleOCR
└───vietocr
```
