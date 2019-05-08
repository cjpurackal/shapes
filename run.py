import matplotlib.pyplot as plt
import numpy as np
import json
import os
import tqdm
import argparse


colors = [
	'blue', 'green', 'red', 'cyan',
	'magenta', 'yellow', 'black', 'white']
task_types = ['classification', 'detection', 'segmentation']
shape_attribs = {'rect': [15, 15], 'circle': [20]}

parser = argparse.ArgumentParser()
parser.add_argument(
		"--save_dir",
		help="path to where you want to save the dataset",
		type=str)
parser.add_argument(
		"--image_size", help="size of the image", nargs='+',
		default=(500, 500), type=int)
parser.add_argument(
		"--num_images", help="number of images for your dataset",
		type=int, default=10)
parser.add_argument(
		"--shapes",
		help="shapes that you require in your dataset. Available: %s"
		% str(list(shape_attribs.keys())),
		nargs='+', default=['circle', 'rect'])
parser.add_argument(
		"--shape_color", help="specify a particular color for all the shapes",
		type=str, default='blue')
parser.add_argument(
		"--shuffle_color", help="shuffle colors for the shapes",
		type=bool, default=False)
parser.add_argument(
		"--task_type", help="specify type of task. Available: %s"
		% str(task_types), type=str, default='detection')


args = parser.parse_args()
image_size = args.image_size
shapes = args.shapes
num_images = args.num_images
save_dir = args.save_dir
shape_color = args.shape_color
shuffle_color = args.shuffle_color
task_type = args.task_type

assert save_dir, "specify save directory"
assert shape_color in colors, "Available colors :"+str(colors)
assert task_type in task_types, "Available task types :"+str(task_types)

# need to make an option for setting up the attribs dynamically
shapes = list(set(shapes))
bbox_label_format = 'bbox'
shuffle_bg = True
shuffle_shape_color = True
image_w = image_size[0]
image_h = image_size[1]
x_white_space = image_w/10
y_white_space = image_h/10
mx = 0
for attr in list(shape_attribs.values()):
	if max(attr) > mx:
		mx = max(attr)
num_rows = int(image_h / (mx))
num_columns = int(image_w / (mx))
# shapes and shape atrribs validation here


def make(x, y, i):
	if shapes[i] == 'rect':
		color = (shuffle_color*colors[np.random.randint(0, 7)]
				+ (1 - shuffle_color)*shape_color)
		return plt.Rectangle(
				(x, y), shape_attribs["rect"][0],
				shape_attribs["rect"][1], color=color)
	elif shapes[i] == 'circle':
		color = (shuffle_color*colors[np.random.randint(0, 7)]
				+ (1 - shuffle_color)*shape_color)
		rad = shape_attribs["circle"][0]
		return plt.Circle((x, y), rad, color=color)


def gen_bbox(x, y, i):
	if shapes[i] == 'rect':
		return {
			'object': 'rect', 'x': x, 'y': y,
			'w': shape_attribs["rect"][0], 'h': shape_attribs["rect"][1]}
	elif shapes[i] == 'circle':
		return {
			'object': 'circle', 'x': x - shape_attribs["circle"][0],
			'y': y - shape_attribs["circle"][0],
			'w': 2 * shape_attribs["circle"][0], 'h': 2 * shape_attribs["circle"][0]}


def detection_gen():
	def make_dirs():
		img_path = os.path.join(save_dir, "dataset", "images")
		lab_path = os.path.join(save_dir, "dataset", "labels_json")
		try:
			os.makedirs(img_path)
		except FileExistsError as e:
			pass
		finally:
			try:
				os.makedirs(lab_path)
			except FileExistsError as e:
				pass
		return img_path, lab_path

	img_path, lab_path = make_dirs()

	for n in tqdm.tqdm(range(num_images)):
		objs = []
		obj_bbox = []
		for row in range(num_rows):
			objs_num = np.random.randint(0, num_columns)
			for i in range(objs_num):
				obj_i = np.random.randint(0, len(shapes))
				# random x, y cord gen
				if np.random.randint(0, 2) * i % 2:
					x = np.random.randint(
							mx * i + (i > 0) * 3 * mx,
							mx * i + (i > 0) * 3 * mx + mx)
					y = np.random.randint(
							mx * (2 * row) + (row > 0) * mx * 3,
							mx * (2 * row) + (row > 0) * mx * 3 + mx)
					objs.append(make(x, y, obj_i))
					obj_bbox.append(gen_bbox(x, y, obj_i))
		fig, ax = plt.subplots(
				figsize=(int(image_w/100), int(image_h/100)))
		ax = fig.add_axes([0, 0, 1, 1])
		ax.set_xlim([0, image_w])
		ax.set_ylim([0, image_h])
		plt.gca().invert_yaxis()

		for i, obj in enumerate(objs):
			ax.add_artist(obj)
		fig.savefig('%s/shapes_%d.png' % (img_path, n))
		with open('%s/shapes_%d.json' % (lab_path, n), 'w') as outfile:
			json.dump(obj_bbox, outfile)

	print ("Generated dataset in %s" % save_dir)


def classification_gen():
	def make_dirs():
		for shape in shapes:
			try:
				os.makedirs(os.path.join(save_dir, "dataset", shape))
			except FileExistsError as e:
				pass
	# image_w = image_h =
	make_dirs()
	for n in tqdm.tqdm(range(num_images)):

		obj_i = int(n/(num_images/len(shapes)))
		if list(shape_attribs.keys())[obj_i] == "rect":
			rect_w = rect_h = np.random.randint(image_w/4, 3*image_w/4)
			shape_attribs["rect"] = [rect_w, rect_h]

			x = np.random.randint(
							0,
							image_w/4)
			y = np.random.randint(
							0,
							image_h/4)
		if list(shape_attribs.keys())[obj_i] == "circle":
			rad = np.random.randint(image_w/8, image_w/4)
			shape_attribs["circle"] = [rad]

			x = np.random.randint(
							2*rad,
							image_w-2*rad)
			y = np.random.randint(
							2*rad,
							image_h-2*rad)
		fig, ax = plt.subplots(
				figsize=(int(image_w/100), int(image_h/100)))
		ax = fig.add_axes([0, 0, 1, 1])
		ax.set_xlim([0, image_w])
		ax.set_ylim([0, image_h])
		plt.gca().invert_yaxis()
		ax.add_artist(make(x, y, obj_i))
		fig.savefig(
			'%s/shapes_%d.png'
			% (os.path.join(save_dir, "dataset", shapes[obj_i]), n))

	print ("Generated dataset in %s" % save_dir)


def segmentation_gen():
	# segmentation and recogition datasets are pretty much the same at this point
	classification_gen()

if task_type == "classification":
	classification_gen()
elif task_type == "detection":
	detection_gen()
elif task_type == "segmentation":
	segmentation_gen()
