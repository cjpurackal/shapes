import matplotlib.pyplot as plt
import numpy as np
import json
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
		"--save_dir", help="For saving the images and labels in a dir",
		type=str)
parser.add_argument(
		"--canvas_size", help="Size of the image", nargs='+',
		default=(500, 500), type=int)
parser.add_argument(
		"--num_images", help="Number of images need in your dataset",
		type=int)
parser.add_argument(
		"--shapes", help="The shapes that you need draw in canvas",
		nargs='+', default=['circle', 'rect', 'circle', 'rect'])
args = parser.parse_args()
canvas_size = args.canvas_size
shapes = args.shapes
shape_attribs = [[20], [15, 15], [40], [30, 50]]
num_images = args.num_images
bbox_label_format = 'bbox'
shuffle_bg = True
shuffle_shape_color = True
canvas_x = canvas_size[0]
canvas_y = canvas_size[1]
x_white_space = canvas_x/10
y_white_space = canvas_y/10
mx = 0
for attr in shape_attribs:
	if max(attr) > mx:
		mx = max(attr)
num_rows = int(canvas_y / (mx))
num_columns = int(canvas_x / (mx))
# shapes and shape atrribs validation here


def make(x, y, i, attr):
	if shapes[i] == 'rect':
		return plt.Rectangle(
				(x, y), shape_attribs[i][0], shape_attribs[i][1])
	elif shapes[i] == 'circle':
		rad = shape_attribs[i][0]
		return plt.Circle((x, y), rad)


def gen_bbox(x, y, i, attr):
	if shapes[i] == 'rect':
		return {
			'object': 'rect', 'x': x, 'y': y,
			'w': shape_attribs[i][0], 'h': shape_attribs[i][1]}
	elif shapes[i] == 'circle':
		return {
			'object': 'circle', 'x': x - shape_attribs[i][0]/2,
			'y': y - shape_attribs[i][0]/2,
			'w': 2 * shape_attribs[i][0], 'h': 2 * shape_attribs[i][0]}


def save_dir(path):
	img_path = os.path.join(path, "dataset", "images")
	lab_path = os.path.join(path, "dataset", "labels_pascalvoc")
	os.makedirs(img_path)
	os.makedirs(lab_path)
	return img_path, lab_path

img_path, lab_path = save_dir(args.save_dir)

debug = True
if debug:
	print ("num_rows : %d" % num_rows)
	print ("num_columns : %d" % num_columns)


for n in range(num_images):
	objs = []
	obj_bbox = []
	for row in range(num_rows):
		objs_num = np.random.randint(0, num_columns)
		for i in range(objs_num):
			obj_i = np.random.randint(0, len(shapes))
			obj_i_attr = shape_attribs[obj_i]
			# random x, y cord gen
			if np.random.randint(0, 2) * i % 2:
				x = np.random.randint(
						mx * i + (i > 0) * 3 * mx,
						mx * i + (i > 0) * 3 * mx + mx)
				y = np.random.randint(
						mx * (2 * row) + (row > 0) * mx * 3,
						mx * (2 * row) + (row > 0) * mx * 3 + mx)
				print ("n : %d x : %d  y : %d"%(n, x, y))
				objs.append(make(x, y, obj_i, obj_i_attr))
				obj_bbox.append(gen_bbox(x, y, obj_i, obj_i_attr))
				# print ("n : %d x : %d  y : %d"%(n, x, y))
				print (obj_bbox)
				# input()
	fig, ax = plt.subplots(
			figsize=(int(canvas_x ), int(canvas_y )))
	ax = fig.add_axes([0, 0, 1, 1])
	ax.set_xlim([0, canvas_x])
	ax.set_ylim([0, canvas_y])
	for i, obj in enumerate(objs):
		ax.add_artist(obj)
	fig.savefig('%s/shapes_%d.png' % (img_path, n))
	with open('%s/shapes_%d.json' % (lab_path, n), 'w') as outfile:
		json.dump(obj_bbox, outfile)

print ("Generated dataset saved in %s" % args.save_dir)
