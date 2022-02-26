# CCPD2VOC
CCPD is Chinese City Parking Dataset.
Each picture in the CCPD dataset contains only one object frame whose name is the License Plate. The object frame information is included in the picture name. We change the picture name to subfolder plus serial number, and propose to generate a file to save new and old names in pair to save the detection box information. Extract the object frame information and generate an XML file corresponding to the new file name. Save to the subfolder of the corresponding picture under the 'annotations' folder. Split into training and evaluation data sets. At this time, CCPD is converted to VOC format dataset, and then it can be trained conveniently. In addition, you can add new object frame information to XML to detect other information of the car.

More about CCPD and download in [https://github.com/detectRecog/CCPD](https://github.com/detectRecog/CCPD) . 
