import numpy as np
import time
import sys
import random

class TSP_solver:
    def __init__(self, distances, init_route, n_cities):
        self.distances = distances
        self.init_route = init_route
        self.best_route = []
        self.n_cities =  n_cities
        self.best_dist = 0

    def update(self, new_route, new_distance):
        self.best_dist = new_distance
        self.best_route = new_route
        return self.best_dist, self.best_route

    def two_opt(self, thr = 0.01):
        self.best_route = self.init_route
        self.best_dist = self.calc_path_dist(self.distances, self.best_route)

        alpha = 1

        while alpha > thr:
            best = self.best_dist
            for city1 in range(self.n_cities - 1):
                for city2 in range(city1+2, self.n_cities-1):
                    edge1_start = self.best_route[city1]
                    edge1_end = self.best_route[city1+1]
                    edge2_start = self.best_route[city2]
                    edge2_end = self.best_route[city2+1]

                    dist1 = self.distances[edge1_start][edge1_end] + self.distances[edge2_start][edge2_end]
                    dist2 = self.distances[edge1_start][edge2_start] + self.distances[edge1_end][edge2_end]
                    if dist2 < dist1:
                        new_route = self.swap(self.best_route, city1, city2)
                        new_distance = self.calc_path_dist(self.distances, new_route)
                        self.update(new_route, new_distance)

            alpha = 1 - self.best_dist/best
        return self.best_route, self.best_dist


    def swap(self,path, city1,city2):
        path_updated = path[0: city1+1] + path[city2:city1:-1] + path[city2+1:]
        return path_updated

    def calc_path_dist(self,distances, route):
        """
        This method calculates the total distance between the first city in the given path to the last city in the path.
        """
        route_dist = 0
        for ind in range(len(route) - 1):
            route_dist += distances[route[ind]][route[ind + 1]]
        return route_dist




if __name__ == '__main__':

    start = time.time()
    # Reading input from file:
    data = open(sys.argv[1], "r").readlines()

    isEuclidean = False

    if(data[0] == "euclidean"):
        isEuclidean = True

    n_cities = int(data[1])

    city_coords = []
    dist_bet_cities = np.zeros((n_cities,n_cities))

    for i in range(n_cities):
        c = [float(x) for x in data[i+2].strip().split(' ')]
        city_coords.append(c)
        d = [float(x) for x in data[n_cities+2+i].strip().split(' ')]
        # print(d)
        dist_bet_cities[i,:] = d
    # loop
    k = 200
    it = 1

    while (time.time() - start) < 290:
        initial_route = list(range(0, n_cities))
        random.shuffle(initial_route)

        tsp = TSP_solver(dist_bet_cities, initial_route, n_cities)
        new_route, new_distance= tsp.two_opt()

        if it == 1:
            best_distance = new_distance
            best_route = new_route
            print(best_distance, best_route)

        if new_distance < best_distance:
            print("-------------")
            print("Iteration:", it)
            best_distance = new_distance
            best_route = new_route
            print(best_distance,"\n","Best_Route:",best_route)
        it += 1


    # print(city_coords)
    # print(data)
    # print(dist_bet_cities)