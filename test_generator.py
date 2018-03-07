import synthetic_generator
import sys
import pytest

def test_divide_fairly():

	groups_unities = synthetic_generator.divide_fairly(3, 0.3, 7, 110)
	answer_unities = [13, 13, 13, 33, 13, 13, 12]
	assert groups_unities == answer_unities

	groups_unities = synthetic_generator.divide_fairly(3, 0.46, 7, 110)
	answer_unities = [10, 10, 10, 50, 10, 10, 10]
	assert groups_unities == answer_unities

	groups_unities = synthetic_generator.divide_fairly(5, 0.31, 7, 109)
	answer_unities = [13, 13, 13, 13, 12, 33, 12]
	assert groups_unities == answer_unities	

	groups_unities = synthetic_generator.divide_fairly(4, 0.31, 7, 109)
	answer_unities = [13, 13, 13, 13, 33, 12, 12]
	assert groups_unities == answer_unities	

	groups_unities = synthetic_generator.divide_fairly(3, 0.101, 10, 110)
	answer_unities = [11 for x in range(10)]
	assert groups_unities == answer_unities	
	

def test_nearest_cloud():

	representatives = [[[2, 3], [50, 70]], [[10, 30], [10, 60], [100, 100]]]
	length = 100
	height = 100
	nearest_cloud = synthetic_generator. \
						get_nearest_cloud(representatives, 1, length, height)
	assert nearest_cloud == 0
	
	representatives[1].append([3, 5])
	
	nearest_cloud = synthetic_generator. \
						get_nearest_cloud(representatives, 1, length, height)
	assert nearest_cloud == 3
	
	representatives[0].append([100, 100])
	nearest_cloud = synthetic_generator. \
						get_nearest_cloud(representatives, 1, length, height)
	assert nearest_cloud == 2
	
	representatives = [[[40, 50], [50, 35]], [[50, 50]], [[30, 50], [50, 30]]]	
	nearest_cloud = synthetic_generator. \
						get_nearest_cloud(representatives, 0, length, height)
	assert nearest_cloud == 1			


def test_generate_point():

	origin = [0, 0]
	topright = [100, 100]
	points = []

	for i in range(1000):	
		point = synthetic_generator. \
					generate_point(origin, topright, [1, 1],
								   [[1, 0], [0, 1]], 'uniform')
		points.append(point)
		point = synthetic_generator. \
					generate_point(origin, topright, origin,
								   [[1, 0], [0, 1]], 'gaussian')
		points.append(point)
		point = synthetic_generator. \
					generate_point(origin, topright, topright,
								   [[1, 0], [0, 1]], 'gaussian')
		points.append(point)
		
	for p in points:												   										   
		assert p[0] >= origin[0] and p[0] <= topright[0] and \
			   p[1] >= origin[1] and p[1] <= topright[1]
		
			   
def test_generate_entity():

	representatives = [[[2, 3], [50, 70]], 
					   [[10, 30], [10, 60], [100, 100]], 
					   [[33, 40], [0, 10], [50, 70], [40, 80]],
					   [[100, 23], [23, 20], [59, 37], [24, 29], [29, 28]], 
					   [[39, 19], [29, 59], [87, 39], [95, 82], [38, 9], 
					   	[100, 99]]]
					   	
	points, points_distr = synthetic_generator. \
						       generate_entity(representatives, 4, 0.325, 0.27, 
										   	   100, 1, 100, 100)
	
	assert points_distr == [-1] * 5 + [0] * 10 + [-1] * 5 + [1] * 10 + \
						   [-1] * 5 + [2] * 10 + [-1] * 5 + [3] * 9 + \
						   [-1] * 4 + [4] * 10 + [-1] * 8 + [5] * 19
						   
	points, points_distr = synthetic_generator. \
						       generate_entity(representatives, 1, 0.399, 
						       				   0.195, 100, 1, 100, 100)
						       				   
	assert points_distr == [-1] * 16 + [0] * 25 + [-1] * 16 + [1] * 24 + \
						   [-1] * 7 + [2] * 12


