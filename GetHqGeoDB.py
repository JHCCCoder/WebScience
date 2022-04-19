import self as self

from NWScore import NWScore

if __name__ == '__main__':
    import json

    with open('data/highFileFeb', 'r') as f:
        HQSet = []
        for line in f.readlines():
            HQSet.append(json.loads(line))

    with open('data/lowFileFeb', 'r') as f:
        LQSet = []
        for line in f.readlines():
            LQSet.append(json.loads(line))

    t = NWScore(HQSet, LQSet)

    samples = []
    with open('data/geoLondonJan', 'r') as f:
        for line in f.readlines():
            samples.append(json.loads(line))

    f = open('HqGeoDB.txt', 'w', newline='\n')

    count = 0
    for sample in samples:
        score = t.GetScore(sample)
        if t.HQTweet(sample):
            count += 1
            f.write(json.dumps(sample) + '\n')
            print(sample)
    f.close()
    print(count)