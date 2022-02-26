
import os
import sys
import cv2
import numpy as np

def one_object_to_xml(xml_file,image_height, image_width,object_data):
    object_name=object_data[0]
    xmin = object_data[1]
    ymin = object_data[2]
    xmax = object_data[3]
    ymax = object_data[4]
    xmin = max(xmin,0)
    ymin = max(ymin, 0)
    xmax = min(xmax,image_width)
    ymax = min(ymax, image_width)
    xmin=int(xmin)
    ymin=int(ymin)
    xmax=int(xmax)
    ymax=int(ymax)



    xml_file.write(' ' * 4 * 1 + '<object>\n')
    xml_file.write(' ' * 4 * 2 + '<name>' + object_name + '</name>\n')
    xml_file.write(' ' * 4 * 2 + '<pose>Unspecified</pose>\n')
    xml_file.write(' ' * 4 * 2 + '<truncated>0</truncated>\n')
    xml_file.write(' ' * 4 * 2 + '<occluded>0</occluded>\n')
    xml_file.write(' ' * 4 * 2 + '<difficult>0</difficult>\n')
    xml_file.write(' ' * 4 * 2 + '<bndbox>\n')
    xml_file.write(' ' * 4 * 3 + '<xmin>' + str(xmin) + '</xmin>\n')
    xml_file.write(' ' * 4 * 3 + '<ymin>' + str(ymin) + '</ymin>\n')
    xml_file.write(' ' * 4 * 3 + '<xmax>' + str(xmax) + '</xmax>\n')
    xml_file.write(' ' * 4 * 3 + '<ymax>' + str(ymax) + '</ymax>\n')
    xml_file.write(' ' * 4 * 2 + '</bndbox>\n')
    xml_file.write(' ' * 4 * 1 + '</object>\n')

def multi_object_to_xml(image_path_in_dataset,image_name,image_style,image_data,xml_path,*object_data):
    [image_height, image_width,image_depth]=image_data
    image_height=int(image_height)
    image_width=int(image_width)
    image_depth=int(image_depth)

    if not os.path.exists(xml_path):
        os.makedirs(xml_path)
    object_num=len(object_data)
    xml_file =open(os.path.join(xml_path,image_name+'.xml'),'w')
    xml_file.write('<annotation>\n')
    xml_file.write(' '*4*1+'<folder>'+image_path_in_dataset+'</folder>\n')
    xml_file.write(' '*4*1+'<filename>'+image_name+'</filename>\n')
    xml_file.write(' '*4*1+'<size>\n')
    xml_file.write(' '*4*2+'<width>'+str(image_width)+'</width>\n')
    xml_file.write(' '*4*2+'<height>' + str(image_height) + '</height>\n')
    xml_file.write(' '*4*2+'<depth>' + str(image_depth) + '</depth>\n')
    xml_file.write(' '*4*1+'</size>\n')
    xml_file.write(' '*4*1+'<segmented>0</segmented>\n')
    if object_num!=0:
        for i in range(object_num):
            one_object_to_xml(xml_file,image_height, image_width, object_data[i])
    xml_file.write('</annotation>')

def add_object_to_xml(image_path_in_dataset,image_name,image_style,image_data,xml_path,*object_data):
    
    [image_height, image_width,image_depth]=image_data
    image_height=int(image_height)
    image_width=int(image_width)
    image_depth=int(image_depth)

    object_num = len(object_data)

    if not os.path.exists(xml_full_path):
        multi_object_to_xml(image_path_in_dataset, image_name, image_style, image_data,xml_path, *object_data)
    else:
    
        xml_full_path_new = os.path.join(xml_path, image_name + '_new.xml')
        xml_file =open(xml_full_path,'r')
        xml_file_list=xml_file.readlines()
        xml_file_list_num=len(xml_file_list)
        #print("xml_file_list",xml_file_list)
        #print("xml_file_list_num", xml_file_list_num)

        xml_file_new = open(xml_full_path_new, 'w')
        for i in range(xml_file_list_num-1):
            xml_file_new.write(xml_file_list[i])

        if object_num!=0:
            for i in range(object_num):
                one_object_to_xml(xml_file_new,image_height, image_width, object_data[i])
        xml_file_new.write('</annotation>')

        xml_file.close()
        xml_file_new.close()
        os.remove(xml_full_path)
        os.rename(xml_full_path_new,xml_full_path)

if __name__ == '__main__':
    image_path='./'
    image_name='road0'
    image_style='.png'
    xml_path='./1'
    object_name='stop'
    xmin=1
    ymin=2
    xmax=3
    ymax=4
    base_path=os.getcwd()
    xml_full_path=os.path.join(xml_path,image_name+'.xml')
    remove_xml=False
    if os.path.exists(xml_full_path) and remove_xml:
        os.remove(xml_full_path)
    object_data1=[object_name,xmin,ymin,xmax,ymax]
    #multi_object_to_xml(image_path,image_name,image_style,xml_path,object_data1,object_data1)
    add_object_to_xml(image_path, image_name, image_style, xml_path, object_data1, object_data1)
    image = cv2.imread('road0.png')
    print(image.shape)

