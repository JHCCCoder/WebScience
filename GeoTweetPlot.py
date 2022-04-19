import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from GeoTweetAllocator import GeoTweetAllocator

class GeoTweetPlot:

    def __init__(self, ):
        self.tweets = []

    def plot_heat_map(grids):
        sns.heatmap(grids, vmax=50, vmin=0)

    def plot_histogram_map(grids):
        grid_units = []
        for rows in grids:
            grid_units.extend([item for item in rows if item != 0])

        plt.figure(figsize=(6, 6), dpi=100)
        plt.hist(grid_units, bins=100)
        plt.gca().set(xlim=(0, 700), ylabel='Number of grids', xlabel='Number of tweets', title='Distribution of '
                                                                                                'Numbers - London')
        plt.tick_params(size=10)
        plt.xticks(np.linspace(0,700,8))

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

        plot_heat_map(Allocator.num_tweets_added)
        plot_histogram_map(Allocator.num_tweets_added)
        plt.show()
