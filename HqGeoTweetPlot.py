import math
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from GeoTweetAllocator import GeoTweetAllocator
from PartitionGrids import PartitionGrids

class PartitionGrids:
    def __init__(self, bounding):
        self.boundingCoordinates = bounding

    def computeDistance(self, long2, lat2):
        R = 6373.0
        lat1 = self.boundingCoordinates[1]
        long1 = self.boundingCoordinates[0]

        phi1 = lat1 * (math.pi / 180)
        phi2 = lat2 * (math.pi / 180)
        delta1 = (lat2 - lat1) * (math.pi / 180)
        delta2 = (long2 - long1) * (math.pi / 180)

        a = math.sin(delta1 / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta2 / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c

        return d

    def createGrid(self):
        self.rows = int(np.ceil(self.computeDistance(self.boundingCoordinates[0], self.boundingCoordinates[3])))
        print(f'number of rows is: {self.rows}')

        self.columns = int(np.ceil(self.computeDistance(self.boundingCoordinates[2], self.boundingCoordinates[1])))
        print(f'number of columns is: {self.columns}')

        self.noofGrids = int(self.rows * self.columns)
        print(f'number of grids is: {self.noofGrids}')

        self.colMax = int(np.ceil(self.computeDistance(self.boundingCoordinates[2], self.boundingCoordinates[1])))
        print(f'number of maximum columns is: {self.colMax}')

        self.rowPoints = []
        self.colPoints = []
        self.lonOffset = (self.boundingCoordinates[2] - self.boundingCoordinates[0]) / self.columns
        self.latOffset = (self.boundingCoordinates[3] - self.boundingCoordinates[1]) / self.rows

        for i in range(self.rows):
            self.rowPoints.append(self.boundingCoordinates[1] + i * self.latOffset)
        for j in range(self.columns):
            self.colPoints.append(self.boundingCoordinates[0] + j * self.lonOffset)

class HqGeoTweetPlot:

    def __init__(self, boundary_coordiantes):
        self.boundary_coordiantes = boundary_coordiantes
        self.tweets = []
        self.grid = PartitionGrids(self.boundary_coordiantes)
        self.grid.createGrid()

        self.rowPoints = self.grid.rowPoints
        self.columnPoints = self.grid.colPoints

        self.num_tweets_added = np.zeros((self.grid.rows, self.grid.columns))
        self.count = 0

    def addTweet(self, tweet):

        if tweet.get('geoenabled', False):
            try:
                lat, lon = self.get_pos(tweet)
                self.count += 1
                if lat > -1 and lon > -1:
                    tweet['lat_index'] = lat
                    tweet['lon_index'] = lon
                    self.num_tweets_added[lat][lon] += 1
            except:
                pass

        self.tweets.append(tweet)

    def get_pos(self, tweet):
        longitude, latitude = tweet['coordinates']['coordinates']
        for i in range(len(self.rowPoints)):
            if latitude < self.rowPoints[i]:
                lat_index = i - 1
                break

        for i in range(len(self.columnPoints)):
            if longitude < self.columnPoints[i]:
                lon_index = i - 1
                break

        return lat_index, lon_index

    def plot_heat_map(grids):
        sns.heatmap(grids, vmax=50, vmin=0)

    def plot_histogram_map(grids):
        grid_units = []
        for rows in grids:
            grid_units.extend([item for item in rows if item != 0])

        plt.figure(figsize=(6, 6), dpi=100)
        plt.hist(grid_units, bins=100)
        plt.gca().set(xlim=(0, 10), ylabel='Number of grids', xlabel='Number of tweets', title='Distribution of '
                                                                                                'Numbers - London')
        plt.tick_params(size=10)
        plt.xticks(np.linspace(0,9,10))

    if __name__ == '__main__':
        samples = []
        with open('data/HqGeoDB.txt', 'r') as f:
            for line in f.readlines():
                samples.append(json.loads(line))

        London = [-0.563, 51.261318, 0.28036, 51.686031]

        Allocator = GeoTweetAllocator(London)
        for sample in samples:
            Allocator.addTweet(sample)

        plot_heat_map(Allocator.num_tweets_added)
        plot_histogram_map(Allocator.num_tweets_added)
        plt.show()
