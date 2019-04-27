import matplotlib.pyplot as plt
import numpy as np
import json
# import argpaser



canvas_size = (500, 500)
shapes = ['circle', 'rect', 'circle', 'rect']
shape_attribs = [[20], [15, 15], [40], [30, 50]]
num_images = 2
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
#shapes and shape atrribs validation here

def make(x, y, i, attr):
	if shapes[i] == 'rect':
		return plt.Rectangle((x, y), shape_attribs[i][0], shape_attribs[i][1])
	elif shapes[i] == 'circle':
		rad = shape_attribs[i][0]
		return plt.Circle((x, y), rad)

def gen_bbox(x, y, i, attr):
	if shapes[i] == 'rect':
		return {'object':'rect','x':x, 'y':y, 'w':shape_attribs[i][0], 'h':shape_attribs[i][1]}
	elif shapes[i] == 'circle':
		return {'object':'circle','x':x - shape_attribs[i][0], 'y':y - shape_attribs[i][0], 'w':2*shape_attribs[i][0], 'h':2*shape_attribs[i][0]}


debug = True
if debug:
	print ("num_rows : %d "%num_rows)
	print ("num_columns : %d"%num_columns) 


for n in range(num_images):
	objs = []
	obj_bbox = []
	for row in range(num_rows):
		objs_num = np.random.randint(0, num_columns)
		for i in range(objs_num):
			obj_i = np.random.randint(0, len(shapes))
			obj_i_attr = shape_attribs[obj_i]
			#random x, y cord gen
			if np.random.randint(0, 2)*i%2:
				x = np.random.randint(mx*i+(i>0)*3*mx, mx*i+(i>0)*3*mx+mx)
				y = np.random.randint(mx*(2*row)+(row>0)*mx*3, mx*(2*row)+(row>0)*mx*3+mx)
				objs.append(make(x, y, obj_i, obj_i_attr))
				obj_bbox.append(gen_bbox(x, y, obj_i, obj_i_attr))
	fig, ax = plt.subplots()
	ax.set_xlim([0, canvas_x])
	ax.set_ylim([0, canvas_y])
	for i, obj in enumerate(objs):
		ax.add_artist(obj)
	fig.savefig('shapes_%d.png'%n)
	with open('shapes_%d.json'%n, 'w') as outfile:
		json.dump(obj_bbox, outfile)
