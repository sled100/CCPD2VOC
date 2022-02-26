# CCPD2VOC
1. CCPD is Chinese City Parking Dataset.
Each picture in the CCPD dataset contains only one object frame whose name is the License Plate. The object frame information is included in the picture name. We change the picture name to subfolder plus serial number, and propose to generate a file to save new and old names in pair to save the detection box information. Extract the object frame information and generate an XML file corresponding to the new file name. Save to the subfolder of the corresponding picture under the 'annotations' folder. Split into training and evaluation data sets. At this time, CCPD is converted to VOC format dataset, and then it can be trained conveniently. In addition, you can add new object frame information to XML to detect other information of the car.


2. object_to_xml.py can generate XML files containing multiple object information or add multiple object information to the XML files of corresponding pictures.

3. prepare_voc_data_for_train.py can collect and save the object frame information, modify the image name of the dataset, generate XML files, segment the dataset, generate train.txt and val.txt and convert it to VOC type dataset. XML files can be generated from the saved object frame information.

4. Object frame information includes [name,xmin,ymin,xmax,ymax]

5. More about CCPD and download in [https://github.com/detectRecog/CCPD](https://github.com/detectRecog/CCPD) . 

# Training with [PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection)
PaddleDetection is an end-to-end object detection development kit based on PaddlePaddle. More about PaddleDetection in [Getting Started](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.3/docs/tutorials/GETTING_STARTED.md).


1. Generate CCPD dataset config file, specify the path for train.txt and val.txt location. copy CCPD to PaddleDetection.

2. Select the object detection network structure and modify the dataset config file in the main config file.
3. Training example.
```bash
!python -u tools/train.py -c configs/yolov3/yolov3_mobilenet_v3_large_ssld_270e_ccpd_voc.yml \
                --use_vdl=true \
                --vdl_log_dir=vdl_dir/scalar \
                --eval
```

4. Detection example
```bash

!python tools/infer.py \
    -c configs/yolov3/yolov3_mobilenet_v3_large_ssld_270e_ccpd_voc.yml \
    -o \
        infer_img=test0.jpg \
        output_dir=output/  \
        weights=output/yolov3_mobilenet_v3_large_ssld_270e_ccpd_voc/best_model \
```
5. Display of test results

Test picture：test0.jpg

Detection result：test0_infer.jpg

Detection frame extraction：test0_frame0.jpg

# Identify with [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
PaddleOCR aims to create multilingual, awesome, leading, and practical OCR tools that help users train better models and apply them into practice. More obout PaddleOCR in [PaddleOCR Quick Start](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.4/doc/doc_en/quickstart_en.md).

1. Download training model
```bash
!wget https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_rec_train.tar
```
2. Unzip training model to PaddleOCR
```bash
infer_path='infer'
if not os.path.exists(infer_path):
    os.mkdir(infer_path) 
!tar -xf ch_ppocr_mobile_v2.0_rec_train.tar -C infer
```
3. Identification detection frame in PaddleOCR.
```bash
!python tools/infer_rec.py \
    -c configs/rec/ch_ppocr_v2.0/rec_chinese_lite_train_v2.0.yml \
    -o \
        Global.pretrained_model=infer/ch_ppocr_mobile_v2.0_rec_train/best_accuracy \
        Global.infer_img=output/test0/test0_frame0.jpg \
```

