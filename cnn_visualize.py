#author: Paulo Henrique Junqueira Amorim

#based on:
#https://machinelearningmastery.com/how-to-visualize-filters-and-feature-maps-in-convolutional-neural-networks/

import os
import sys
import imageio
from numpy import expand_dims
import argparse

import html_template as ht

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import Model

IMG_FOLDER_FILTERS = '/img_filters/'
IMG_FOLDER_FEATURES = '/img_feature/'

def write_html_filter(files_path, html_path):
    html_file = open(html_path, 'w+')
 
    layers_html = ''
    for layer in files_path:
        
        if layer != []:
            
            filters_html = ''
            for filters in layer:

                    cell_line = ''
                    for channel_file in filters:
                        channel_file = '.' + IMG_FOLDER_FILTERS + os.path.basename(channel_file)
                        cell_line += ht.cell(channel_file)
                    
                    filters_html += ht.row(cell_line)
                  
    html = ht.table(filters_html)

    html_file.write(html)

def write_html_feature(all_features, layer_detail, html_path):
    html_file = open(html_path, 'w+')
    ld=0
    filters_html = ''
    for ft in all_features:
        cell_line = ''
        cell_line += ht.cell(None, layer_detail[ld])
        for f in ft:
            f_file = '.' + IMG_FOLDER_FEATURES + os.path.basename(f)
            cell_line += ht.cell(f_file)
        ld += 1            
        filters_html += ht.row(cell_line)
                  
    html = ht.table(filters_html)

    html_file.write(html)

def filter_visualize(model, layer_number, out_dir):
    """
    Visualize convolutional filters from layers. 
    model (a keras model) 
    layer_number=1 (default first layer), -1 (to visualize all layers)
    """
    i_layer = 1
    layer_ = []

    for layer in model.layers:

        if 'conv' in  layer.name:
            filters, biases = layer.get_weights()

            fshape = filters.shape
            n_filters = fshape[-1]
            depth = fshape[-2]
           
            #normalize 0-1
            f_min, f_max = filters.min(), filters.max()
            filters = (filters - f_min) / (f_max - f_min)
           
            filters_ = []
            ix = 1
            for i in range(n_filters):
                
                # get the filter
                f = filters[:, :, :, i]
                
                # plot each channel separately
                channels_ = []
                for j in range(depth):
                   
                    if layer_number != -1:

                        if i_layer == layer_number:
                            fname = str(i_layer) + '_' + str(ix) + '_'\
                                    + str(j) + '.png'
                            
                            fpath = os.path.join(out_dir,fname)
                            imageio.imsave(fpath, f[:,:,j])

                            channels_.append(fpath)
                    ix += 1

                if layer_number != -1:
                    if i_layer == layer_number:
                        filters_.append(channels_)
    
            i_layer += 1
            layer_.append(filters_)
    
    return layer_


def feature_visualize(model, outputs_i, img, out_dir):
    
    outputs = []
    for i in outputs_i:
        outputs.append(model.layers[i].output)
    
    model = Model(inputs=model.inputs, outputs=outputs)

    # expand dimensions so that it represents a single 'sample'
    img = expand_dims(img, axis=0)

    # prepare the image (e.g. scale pixel values for the vgg)
    img = preprocess_input(img)
    
    # get feature map for first hidden layer
    feature_maps = model.predict(img)
    
    nf = 0 
    all_features = []
    for fmap in feature_maps:
        features = []
        for ix in range(fmap.shape[-1]):
            fname =  str(nf) + '_' + str(ix) + '.png'
            fpath = os.path.join(out_dir,fname)
            imageio.imsave(fpath, fmap[0, :, :, ix])
            features.append(fpath)
        nf+=1
        all_features.append(features)

    return all_features

def get_filters(model):
    
    filters_ = []
    n = 1
    for layer in model.layers:
        if 'conv' not in layer.name:
            continue
        filters, biases = layer.get_weights()
        filters_.append((n, layer.name, filters.shape))
        n += 1
    
    return filters_

def get_features(model):

    features = []
    # summarize feature map shapes
    for i in range(len(model.layers)):
        layer = model.layers[i]
        # check for convolutional layer
        if 'conv' not in layer.name:
            continue
        # summarize output shape
        features.append((i, layer.name, layer.output.shape))

    return features


if __name__ == '__main__':

    #**** Change for your model ****
    model = VGG16()

    parser = argparse.ArgumentParser(description='Visualize filter or\
            features from CNN models.')
    
    parser.add_argument('-o','--output', dest='out_dir',\
            type=str, help='A folder path to output html page', required=False) 

    parser.add_argument('-t','--type', dest='out_type',\
            type=int, help='1 - Output features (default) \n 2 - Output filters',\
            required=False) 

    parser.add_argument('-i','--img', dest='img_path',\
            type=int, help='Image input to generate CNN features',\
            required=False) 

    parser.add_argument('-l','--layer', dest='filter_number',\
            type=int, help='Filter number to save (default 1)',\
            required=False) 


    args = parser.parse_args()
    
    if args.out_dir:
        out_dir = args.out_dir
    else:
        out_dir = os.path.abspath('./html_output/')

    if args.out_type:
        out_type = args.out_type
    else:
        out_type = 1

    if args.img_path:
        img_path = args.img_path
    else:
        img_path = os.path.abspath('./bird.jpg')

    if args.filter_number:
        filter_number = args.filter_number
    else:
        filter_number = 1

    if out_type == 1:

        # *** Change for your target_size (VGG16 is 224x224 Input) ***
        img = load_img(img_path, target_size=(224, 224))
        
        # convert the image to an array
        img = img_to_array(img)

        out_dir = out_dir + IMG_FOLDER_FEATURES

        if not(os.path.exists(out_dir)):
            os.makedirs(out_dir)

        features = get_features(model)
        
        outputs_i = []
        layer_detail = []
        for f in features:
            outputs_i.append(f[0])
            print(f)
            layer_detail.append([f[0], f[1], f[2][1], f[2][2], f[2][3]])

        all_features = feature_visualize(model, outputs_i, img, out_dir)
        html_path = os.path.join(os.path.abspath(os.path.join(out_dir,"../")),\
                'features.html')

        write_html_feature(all_features, layer_detail, html_path)
        
        
    else:

        out_dir = out_dir + IMG_FOLDER_FILTERS
        
        if not(os.path.exists(out_dir)):
            os.makedirs(out_dir)
        
        filters = get_filters(model)
        print("Filters:\n")
        for f in filters:
            print(f)

        print("Generate filter number", str(filter_number), '\n')
        file_list = filter_visualize(model, int(filter_number), out_dir)
        html_path = os.path.join(os.path.abspath(os.path.join(out_dir,"../")),'filters.html')
        write_html_filter(file_list, html_path)


