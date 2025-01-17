#This file is the file that you need to change. Here, we define the K-means class.
"""

The functions
1. distance
2. cal_distortion
3. cluster

need to be completed.

"""
import numpy as np

class Kmeans:
    def __init__(self):

        self.K = None       #No. of Clusters
        self.N = None       #No. of Data Points
        self.M = None       #No. of Dimensions
        self.T = None       #No. of Iterations

        self.centroids = None       #List of centers of cluster
        self.labels = None          #List of labels for each data point
        self.distortion = None      #Distortion


    def distance(self, data_point, centroid):
        """
        Function to calculate distance.
        :param data_point: a vector in R^M space, the data point in consideration.
        :param centroid: a vector in R^M space, the centroid in consideration.
        :return: the euclidean distance between these two vectors.
        """
        #The distance to be minimized between the centroid and the data_point needs to be defined here.
        Distance = 0
        Distance = np.linalg.norm(data_point - centroid)


        #Write your code above.
        # Calculate Distance b/w data_point and centroid here.
        return Distance

    def cluster(self, feature_vector, k, verbose = True, n_iterations = 20):
        """
        Function that implements the kmeans clustering algorithm.
        :param feature_vector:   N x M vector, the dataset provided.
        :param k: No. of clusters, an integer
        :param verbose:  boolean variable, defines verbosity.
        :param n_iterations: No. of iterations, an integer
        :return:   Nothing. But after running this function self.labels, self.centroids, self.distortion variables should be calculated

        """
        self.N = feature_vector.shape[0]
        self.M = feature_vector.shape[1]
        self.K = k
        self.T = n_iterations

        indices = np.random.choice(self.N, self.K, replace = False)     #initializing the centroids randomly
        self.centroids = feature_vector[indices]
        self.labels = np.zeros(self.N)

        for iterator in range(self.T):
            self.clusters = {}
            for i in range(self.K):
                self.clusters[i] = []
            for i, feature in enumerate(feature_vector):
                distance = []
                for centroid in self.centroids:
                    distance.append(self.distance(feature, centroid))
                min_distance = min(distance)
                self.labels[i] = distance.index(min_distance)
                self.clusters[self.labels[i]].append(feature)
            for i in range(self.K):
                self.centroids[i] = np.mean(self.clusters[i], axis=0)


            # Calcluate self.labels above
            # write your code above
            self.cal_distortion(feature_vector)
            if verbose:
                print("Distortion after ", iterator + 1 ," iterations is ", self.distortion)



            # Calculate self.centroids above
            # write your code above
    def cal_distortion(self, feature_vector):
        """
        Function to calcluate distortion.
        :param feature_vector: N x M vector, the dataset provided.
        :return: Nothing.  But after the execution of this function, self.distortion should be updated.
        Distortion: the sum of squared distances of all the data points with their respective centers.
        """
        distortion = 0
        for i in range(self.K):
            for feature in self.clusters[i]:
                distortion += self.distance(feature, self.centroids[i]) ** 2
        self.distortion = distortion



        # calculate self.distortion above.