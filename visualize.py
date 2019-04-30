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

	fig, ax = plt.subplots(1)
	print (boxes)
	ax.imshow(img)
	for i in range(len(boxes)):
		k = 0
		s = plt.Rectangle(
				(boxes[i][k], boxes[i][k+1]), boxes[i][k+2],
				boxes[i][k+3], linewidth=1, edgecolor='g',
				facecolor="none")
		ax.add_patch(s)
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
			"--save_dir", help="dataset path to be visualize")
	args = parser.parse_args()
	bounding_boxes(args.save_dir)
