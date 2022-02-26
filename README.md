# CCPD2VOC
CCPD is Chinese City Parking Dataset.
Each picture in the CCPD dataset contains only one object frame whose name is the License Plate. The object frame information is included in the picture name. We change the picture name to subfolder plus serial number, and propose to generate a file to save new and old names in pair to save the detection box information. Extract the object frame information and generate an XML file corresponding to the new file name. Save to the subfolder of the corresponding picture under the 'annotations' folder. Split into training and evaluation data sets. At this time, CCPD is converted to VOC format dataset, and then it can be trained conveniently. In addition, you can add new object frame information to XML to detect other information of the car.


object_to_xml.py can generate XML files containing multiple object information or add multiple object information to the XML files of corresponding pictures.
prepare_voc_data_for_train.py can collect and save the object frame information, modify the image name of the dataset, generate XML files, segment the dataset and convert it to VOC type dataset. XML files can be generated from the saved object frame information.

Object frame information includes [name,xmin,ymin,xmax,ymax]

More about CCPD and download in [https://github.com/detectRecog/CCPD](https://github.com/detectRecog/CCPD) . 

# [PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection)
```bash

```

