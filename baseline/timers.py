from __future__ import print_function
import os
import time
from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def kmeans_baseline(data, n, filename):
    """
    Fit data to a K-means model with n clusters and record processing time to a csv file.

    :param data: Numpy array with data to classify
    :param n: Number of clusters to generated
    :return: Processing time (in seconds)
    """

    k_means = KMeans(n_clusters=n, init='k-means++', n_init=10)

    t0 = time.time()
    k_means.fit(data)
    t1 = time.time() - t0

    project = os.path.realpath('.')
    csv = os.path.join(project, filename)

    if not os.path.exists(csv):
        with open(csv, mode='w') as timing:
            timing.write('clusters,seconds\n')

    with open(csv, mode='a') as timing:
        timing.write('{},{}\n'.format(n, t1))

    print('K-means: {} clusters, {} seconds'.format(n, t1))

    return t1


def dbscan_baseline(data, eps, samples, filename):

    dbscan = DBSCAN(eps=eps,
                    min_samples=samples)

    t0 = time.time()
    dbscan.fit(data)
    t1 = time.time() - t0

    clusters = dbscan.labels_.unique()

    project = os.path.realpath('.')
    csv = os.path.join(project, filename)

    if not os.path.exists(csv):
        with open(csv, mode='w') as timing:
            timing.write('espilon,samples,clusters,seconds\n')

    with open(csv, mode='a') as timing:
        timing.write('{},{},{},{}\n'.format(eps, samples, clusters, t1))

    print('DBSCAN: epsilon={}, {} clusters, {} seconds'.format(eps, clusters, t1))

    return t1


def minibatch_timing(data, n, batch_size, filename):
    """
    Fit data to a minibatch K-means model with n clusters and record processing time to a csv file.

    :param data: Numpy array with data to classify
    :param n: Number of clusters to generated
    :param batch_size: Desired batch size
    :return: Processing time (in seconds)
    """

    mb = MiniBatchKMeans(n_clusters=n, init='k-means++', n_init=10, batch_size=batch_size, init_size=max(30, n))

    t0 = time.time()
    mb.fit(data)
    t1 = time.time() - t0

    project = os.path.realpath('.')
    csv = os.path.join(project, filename)

    if not os.path.exists(csv):
        with open(csv, mode='w') as timing:
            timing.write('clusters,seconds,batchsize\n')

    with open(csv, mode='a') as timing:
        timing.write('{},{}\n'.format(n, t1, batch_size))

    print('Minibatch K-means: {} clusters, {} seconds, {} batch size'.format(n, t1, batch_size))

    return t1