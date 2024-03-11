import math

def bucket(l, buckets=None):
    if buckets == None:
        buckets = math.ceil(len(l) / 10)
    data_min = min(l)
    data_max = max(l)
    data_range = data_max - data_min
    bucket_size = data_range / buckets * 1.001
    result = [0 for _ in range(buckets)]
    for i in l:
        index = math.floor((i - data_min) / bucket_size)
        result[index] += 1
    return result
