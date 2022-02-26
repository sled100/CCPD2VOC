# 转换检测数据
import numpy as np
import os, cv2
import random
from object_to_xml import multi_object_to_xml,one_object_to_xml


paths=[]
base_path=os.path.join('CCPD2019')
file_list = os.listdir(base_path)
print('len(file_list ):',len(file_list))
for i in range(len(file_list)):
    if file_list[i].startswith('ccpd'):
        paths.append(file_list[i])
print('paths',paths)
def ccpd_to_voc(base_path):
    paths = []
    file_list = os.listdir(base_path)
    image_id_pair='image_id_pair'
    image_id_file=open(os.path.join(base_path,image_id_pair+'.txt'),'a')
    print('len(file_list ):', len(file_list))
    for i in range(len(file_list)):
        if file_list[i].startswith('ccpd_'):
            paths.append(file_list[i])
    #paths = ['ccpd_weather']
    for path in paths:
        print('path:',path)
        image_num=0
        image_list_in_path=os.listdir(os.path.join(base_path,path))
        image_list_in_path_num=len(image_list_in_path)
        print('image_list_in_path_num:',image_list_in_path_num)
        for i in range(image_list_in_path_num):
            #print('image_list_in_path[i]:',image_list_in_path[i])
            if image_list_in_path[i].startswith('ccpd_'):
                #print('image_list_in_path[i]:',image_list_in_path[i])
                image_num+=1
        print('image_new_num:',image_num)

        
        for item in os.listdir(os.path.join(base_path, path)):
            if len(item.split('-'))!=7:
                continue
            else:
                _, _, bbox, points, label, _, _ = item.split('-')
                points = points.split('_')
                points = [_.split('&') for _ in points]
                tmp = points[-2:]+points[:2]
                points = []
                for point in tmp:
                    points.append([int(_) for _ in point])
                #print('points:',points,np.shape(points),np.max(points,axis=0))

                image_path = os.path.join(base_path,path)
                #print('path,item:',path,item)
                image_name,image_style = item.split('.')
                image_style='.'+image_style
                #print('image_name,image_style:', image_name,image_style)
                #print('image_path+image_name+image_style:',image_path+image_name+image_style)
                image_full_path_old=os.path.join(base_path,path,item)
                image_full_path_new=os.path.join(base_path,path,path+str(image_num)+image_style)
                image_id_pair_line=path+str(image_num)+' '+image_full_path_old+'\n'
                image_id_file.write(image_id_pair_line)

                #print('image_full_path_new:',image_full_path_new)
                assert not os.path.exists(image_full_path_new),print('error:the image_full_path_new is incorrect')
                os.rename(image_full_path_old,image_full_path_new)

                image_name_new=path+str(image_num)
                image_path_in_dataset=path
                xml_path = os.path.join(base_path,'annotations',path)
                object_name = 'License_Plate'
                xmin,ymin = np.min(points,axis=0)
                xmax,ymax = np.max(points,axis=0)
                object_data = [object_name, xmin, ymin, xmax, ymax]
                #image_height, image_width,image_depth=1160,720,3
                
                image = cv2.imread(image_full_path_new)
                #print(image)
                #print('in multi_object_to_xml,image_full_path:',image_full_path)
                image_height, image_width,image_depth=image.shape
                image_data=[image_height, image_width,image_depth]
                multi_object_to_xml(image_path_in_dataset,image_name_new,image_style,image_data,xml_path,object_data)

                image_num+=1

    image_id_file.close()

def ccpd_list_pair_to_voc(base_path):
    paths = []
    file_list = os.listdir(base_path)
    image_id_pair='image_id_pair'
    image_id_pair_path=os.path.join(base_path,image_id_pair+'.txt')
    image_id_pair_file=open(image_id_pair_path,'r')
    image_id_pair_file_list=image_id_pair_file.readlines()
    image_id_pair_file.close()

    print('image_id_pair_path:', image_id_pair_path)
    
    image_id_pair_file_list_num=len(image_id_pair_file_list)
    print('len(image_id_pair_file_list):', image_id_pair_file_list_num)

    for i in range(image_id_pair_file_list_num):
        image_name_new,image_full_path_old=image_id_pair_file_list[i].split(' ')
        base_path,path,item=image_full_path_old.split('/')
        #print(image_name_new)
        if len(item.split('-'))!=7:
                continue
        else:
            _, _, bbox, points, label, _, _ = item.split('-')
            points = points.split('_')
            points = [_.split('&') for _ in points]
            tmp = points[-2:]+points[:2]
            points = []
            for point in tmp:
                points.append([int(_) for _ in point])
            #print('points:',points,np.shape(points),np.max(points,axis=0))

            #print('path,item:',path,item)
            image_name,image_style = item.split('.')
            image_style='.'+image_style[:-1]#remove '\n'
            #print('image_name,image_style:', image_name,image_style)
            image_full_path_new=os.path.join(base_path,path,image_name_new+image_style)
                
            image_path_in_dataset=os.path.join(base_path,path)
            xml_path = os.path.join(base_path,'annotations',path)
            object_name = 'License_Plate'
            xmin,ymin = np.min(points,axis=0)
            xmax,ymax = np.max(points,axis=0)
            object_data = [object_name, xmin, ymin, xmax, ymax]
            image_height, image_width,image_depth=1160,720,3
            image_data=[image_height, image_width,image_depth]
            #image = cv2.imread(image_full_path)
            #print(image)
            #print('in multi_object_to_xml,image_full_path:',image_full_path)
            #image_height, image_width,image_depth=image.shape
            multi_object_to_xml(image_path_in_dataset,image_name_new,image_style,image_data,xml_path,object_data)

    
    

def separate_ccpd_dataset(base_path,object_name):
    image_list=[]
    paths=[]
    file_list = os.listdir(base_path)
    print('len(file_list ):', len(file_list))
    for i in range(len(file_list)):
        if file_list[i].startswith('ccpd_'):
            paths.append(file_list[i])
    #paths=['ccpd_weather']
    for path in paths:
        for item in os.listdir(os.path.join(base_path, path)):
            image_path = os.path.join(base_path,path, item)
            image_path_in_dataset = os.path.join(path, item)
            #xml_path = base_path + 'annotations/' + path + '/'+item
            image_name,_=item.split('.')
            xml_path = os.path.join(base_path, 'annotations',path,image_name+'.xml')
            xml_path_in_dataset = os.path.join('annotations',path,image_name+'.xml')
            image_xml_pair= './'+image_path_in_dataset+'\t'+'./'+xml_path_in_dataset+'\n'
            #print('image_xml_pair:',image_xml_pair)

            image_list.append(image_xml_pair)

    random.shuffle(image_list)
    with open(os.path.join(base_path,'train.txt'), 'w', encoding='UTF-8') as f:
        for image in image_list[:-1431]:
            f.write(image)

    with open(os.path.join(base_path,'val.txt'), 'w', encoding='UTF-8') as f:
        for image in image_list[-1431:]:
            f.write(image)
    with open(os.path.join(base_path,'label_list.txt'), 'w', encoding='UTF-8') as f:
        f.write(object_name + '\n')

if __name__ == '__main__':
    base_path=os.path.join('CCPD2019')
    object_name = 'License_Plate'
    #ccpd_to_voc(base_path)
    ccpd_list_pair_to_voc(base_path)
    #separate_ccpd_dataset(base_path,object_name)
