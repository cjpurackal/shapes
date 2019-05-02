# shapes :large_blue_circle: :large_orange_diamond: :small_red_triangle: :red_circle:
A dataset generator for validating computer vision models for classification, detection and segmentation before testing it out with real world datasets

# Usage

Generate a dataset of circles and rectangles with bounding boxes
```
python run.py --save_dir /tmp/ --image_size 500 500 --num_images 5 --shapes circle rect
```

Or you can run simply with defualt config
```
 python run.py --save_dir /tmp/
```

# Visualize 

Visualize the generated dataset
```
python visualize.py --dataset_dir /tmp/dataset
```
![](imgs/shapes_1.png)
![](imgs/shapes_2.png)