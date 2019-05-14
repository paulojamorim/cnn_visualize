#author: Paulo Henrique Junqueira Amorim

#based on:
#https://machinelearningmastery.com/how-to-visualize-filters-and-feature-maps-in-convolutional-neural-networks/

import os
import sys
import imageio
import html_template as ht

from keras.applications.vgg16 import VGG16

IMG_FOLDER = '/img/'

def write_html(files_path, html_path):
    html_file = open(html_path, 'w+')
 
    layers_html = ''
    for layer in files_path:
        
        if layer != []:
            
            filters_html = ''
            for filters in layer:

                    cell_line = ''
                    for channel_file in filters:
                        channel_file = '.' + IMG_FOLDER + os.path.basename(channel_file)
                        cell_line += ht.cell(channel_file)
                    
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
                            fname = str(i_layer) + '_' + str(ix) + '_' + str(j) + '.png'
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

if __name__ == '__main__':

    #Change for your model
    model = VGG16()
    
    out_dir = os.path.abspath(sys.argv[1]) + IMG_FOLDER
    
    if not(os.path.exists(out_dir)):
        os.makedirs(out_dir)
    
    filters = get_filters(model)
    for f in filters:
        print(f)

    filter_number = input('Select the filter number to generate visualization: ')

    file_list = filter_visualize(model, int(filter_number), out_dir)
    html_path = os.path.join(os.path.abspath(os.path.join(out_dir,"../")),'index.html')
    write_html(file_list, html_path)
