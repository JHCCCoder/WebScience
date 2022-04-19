import numpy as np

from PartitionGrids import PartitionGrids

class GeoTweetAllocator:
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

if __name__ == '__main__':
    import json
    samples = []
    with open('data/geoLondonJan', 'r') as f:
        for line in f.readlines():
            samples.append(json.loads(line))

    London = [-0.563, 51.261318, 0.28036, 51.686031]

    Allocator = GeoTweetAllocator(London)
    for sample in samples:
        Allocator.addTweet(sample)