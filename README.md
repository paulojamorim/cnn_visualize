# CNN Visualize
Display filters or features map of Convolutional Neural Networks (CNN) models of Keras in a HTML page.

## To run

#### Because of the amount of images normally generated it is recommended to view in Firefox.

### Run examples:

### Visualize features
```
 python cnn_visualize.py -t 1 -i ./bird.jpg
 ```

![Features](https://raw.githubusercontent.com/paulojamorim/cnn_visualize/master/img_features.png)

### Visualize filters

```
python cnn_visualize.py -t 2 -l 2

```
![Filters](https://raw.githubusercontent.com/paulojamorim/cnn_visualize/master/img_filters.png)

## Arguments:

```
  -h, --help            show this help message and exit
  -o OUT_DIR, --output OUT_DIR
                        A folder path to output html page
  -t OUT_TYPE, --type OUT_TYPE
                        1 - Output features (default) 2 - Output filters
  -i IMG_PATH, --img IMG_PATH
                        Image input to generate CNN features
  -l FILTER_NUMBER, --layer FILTER_NUMBER
                        Filter number to save (default 1)
```

## Changing to your model:

Change to your model:

```
179:  model = VGG16()
```
Change target_size to your input size:

```
225:  img = load_img(img_path, target_size=(224, 224))
```
