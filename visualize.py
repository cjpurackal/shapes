import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import os
import argparse


def json_listing(json_data):
	label = []
	for region in json_data:
		label.append(
			[region['x'], region['y'], region['w'], region['h']])
	return label


def bbox_plot(img, boxes):

	fig, ax = plt.subplots(
			figsize=(int(500/100), int(500/100)))
	ax.set_xlim([0, 500])
	ax.set_ylim([0, 500])
	plt.gca().invert_yaxis()
	ax.imshow(img)
	objs = []
	for i in range(len(boxes)):
		objs.append(plt.Rectangle(
				(boxes[i][0], boxes[i][1]), boxes[i][2],
				boxes[i][3], linewidth=1, edgecolor='g',
				facecolor="none"))
	for i, obj in enumerate(objs):
		ax.add_artist(obj)
	plt.show()


def bounding_boxes(path):

	img_path, lab_path = os.listdir(path)
	img_path = os.path.join(path, img_path)
	lab_path = os.path.join(path, lab_path)
	img_list = sorted(os.listdir(img_path))
	lab_list = sorted(os.listdir(lab_path))
	for im, lab in zip(img_list, lab_list):
		img = plt.imread(os.path.join(img_path, im))
		print (im)
		print (lab)
		with open(os.path.join(lab_path, lab), 'r') as json_data:
			json_data = json.load(json_data)
			box_list = json_listing(json_data)
		bbox_plot(img, box_list)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument(
			"--dataset_dir", help="dataset path to be visualize")
	args = parser.parse_args()
	bounding_boxes(args.dataset_dir)
