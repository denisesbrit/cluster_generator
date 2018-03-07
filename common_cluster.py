import sys
import math
import numpy as np
import synthetic_generator

CONTROL = 2		
CLOUDS_CONTROL = 2
CLOUDS_SUPER = 4			

def merge_intervals(intervals):

	intervals[:] = sorted(intervals)
	i = 0
	
	while i < len(intervals) - 1:
	
		if intervals[i][1] < intervals[i + 1][0]:  # empty intersection
			i += 1
			
		else:
			if intervals[i][1] < intervals[i + 1][1]:   # i + 1 extends i
				intervals[i][1] = intervals[i + 1][1]
				
			# another possibility: i + 1 contained in i
			
			intervals[:] = intervals[:i + 1] + intervals[i + 2:]
			
			
def complement_intervals(intervals, min_lim, max_lim):

	complement_intervals = []
	
	if intervals[0][0] > min_lim:
		complement_intervals.append([min_lim, intervals[0][0]])
		
	for i in range(len(intervals) - 1):
		complement_intervals.append([intervals[i][1], intervals[i + 1][0]])
		
	if intervals[-1][1] < max_lim:
		complement_intervals.append([intervals[-1][1], max_lim])
	
	intervals[:] = complement_intervals
		
		
def generate_clouds(representatives, cluster_type, nclouds, delta, length,
					height):

	origin = [0, 0]
	topright = [length, height]
	index = len(representatives)
	newrepresentative = []
	
	if cluster_type == 'common':
		shape = (nclouds, len(origin))
		newrepresentative = np.random.uniform(origin, topright, shape).tolist()
		
	else:  # 'super' or 'control'
		intervals = [[], []]
		
		for i in range(len(representatives)):
		
			for j in range(len(representatives[i])):
			
				for dim in range(len(representatives[i][j])):
					center = representatives[i][j][dim]
					newinterval = [max(center - 3 * delta, origin[dim]),
								   min(center + 3 * delta, topright[dim])]
					intervals[dim].append(newinterval)
		
		for dim in range(len(intervals)):
			merge_intervals(intervals[dim])	
			complement_intervals(intervals[dim], origin[dim], 
								 topright[dim])	

		for i in range(nclouds):
			newcloud = []
			
			for dim in range(len(intervals)):
				numintervals = len(intervals[dim])
				index_interval = np.random.choice(numintervals)
				sample_interval = intervals[dim][index_interval]
				newcloud.append(np.random.uniform(sample_interval[0], 
												  sample_interval[1]))
												  
			newrepresentative.append(newcloud)
		
	return newrepresentative


def generate_representatives(numclusters, numclouds, delta, length, height):
	
	representatives = []
	superclusters = numclusters - CONTROL - 1  # 1 for the common cluster
	newclouds = []
	
	for i in range(numclusters):
	
		if i == 0:  # common cluster
			nclouds = numclouds
			cluster_type = 'common'
		elif i < superclusters + 1:  # superclusters
			nclouds = CLOUDS_SUPER - numclouds
			cluster_type = 'super'
		else:  # control clusters
			nclouds = CLOUDS_CONTROL
			cluster_type = 'control'
			
		new_representative = generate_clouds(representatives, cluster_type,
											 nclouds, delta, length, height)
		
		if i > 0 and i < superclusters + 1:  # superclusters
			new_representative += representatives[0]  # add common clouds
		
		representatives.append(new_representative)
	
	print representatives
	return representatives


def generate_entity(representatives, index, cloud_balance, numclouds, 
					numpoints, delta, length, height):
	
	points = []
	points_distr = []
	origin = [0, 0]
	topright = [length, height]
	curr_representative = representatives[index]
	numclusters = len(representatives)
	superclusters = numclusters - CONTROL - 1  # 1 for the common cluster

	if index == 0 or index > superclusters:
	
		if index == 0:  # common cluster
			nclouds = numclouds
		else:  # control clusters
			nclouds = CLOUDS_CONTROL
			
		#uniform division
		npoints = synthetic_generator.divide_fairly(0, 1 / float(nclouds),
													nclouds, numpoints)
			
	else:  # superclusters
		nclouds = CLOUDS_SUPER
		nsubcluster = int(math.floor(numpoints * cloud_balance))
		
		# common clouds were added at the end
		npoints = synthetic_generator. \
					divide_fairly(-1, 1 / float(numclouds), numclouds,
								  nsubcluster)

		rest = numpoints - sum(npoints)
		rest_npoints = synthetic_generator. \
						divide_fairly(0, 1 / float(nclouds - numclouds),
									  nclouds - numclouds, rest)
		npoints = rest_npoints + npoints
	
	for i in range(nclouds):
		mean = curr_representative[i]
		cov = [[delta, 0], [0, delta]]

		for j in range(npoints[i]):
			newpoint = synthetic_generator. \
							generate_point(origin, topright, mean, cov, 
						   				  	   'gaussian')	
			points_distr.append(i)  # mark the corresponding cloud
			points.append(newpoint)	
			
	return points, points_distr		

	
def generate_entities(representatives, cluster_balance, cloud_balance,
					  numclouds, numentities, numpoints, length, height):
	"""
	"""			  
	numclusters = len(representatives)
	clusters = [[] for x in range(numclusters)]
	main_cluster = 0

	nentities = synthetic_generator. \
					divide_fairly(main_cluster, cluster_balance, numclusters,
								  numentities)
								  
	for i in range(numclusters):
		curr_nentities = nentities[i]
					
		for j in range(curr_nentities):
			new_entity, entity_distr = generate_entity(representatives, i, 
													   cloud_balance,
													   numclouds, numpoints,
													   delta, length, height)
			clusters[i].append(new_entity)
				
	return clusters



if __name__ == '__main__':

	numclusters = int(sys.argv[1])  # 2 of them are control
	numclouds = int(sys.argv[2])  # number of clouds that are shared
	cluster_balance = float(sys.argv[3])  # % entities in the dominant cluster
	cloud_balance = float(sys.argv[4])  # % points in the common clouds
	seed = int(sys.argv[5])
	numentities = int(sys.argv[6])
	numpoints = int(sys.argv[7])
	delta = float(sys.argv[8])  # just to tell what configures a diff. cluster
	length = float(sys.argv[9])
	height = float(sys.argv[10])
	outfile_name = sys.argv[11]
	
	np.random.seed(seed)
	
	representatives = generate_representatives(numclusters, numclouds, delta, 
											   length, height)

	clusters = generate_entities(representatives, cluster_balance, 
								 cloud_balance, numclouds, numentities,
								 numpoints, length, height)
	synthetic_generator.print_entities(clusters, outfile_name)
	synthetic_generator.plot_data(clusters, outfile_name + '_plot', length,
								  height)
	
