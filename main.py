import math
import os
from random import sample
import cPickle as pickle

from scipy import spatial
from PIL import Image
import numpy as np
import indicoio

# number of images to compare with input for match
N_IMG = 500
indicoio.config.api_key = '849d554c008efc8d86fbf0c792daba2e'
api_key='849d554c008efc8d86fbf0c792daba2e'
def make_paths_list():
    d = []

    i = 0
    for root, dirs, files in os.walk("clothing_images"):
        for image in files:
            if image.endswith(".jpg"):
                d.append(os.path.join(root, image))
                i += 1
                if i == N_IMG:
                    return d



def make_feats(paths):
    return indicoio.image_features(paths,api_key, batch=True, v=3)
    pass


def calculate_sim(feats):
    distances = spatial.distance.pdist(np.matrix(feats), 'euclidean')
    m = []
    q = lambda i,j,n: n*(n-1)/2 - (n-i)*(n-i-1)/2 + j - i - 1
    for i in range(N_IMG):
        r = []
        for j in range(N_IMG):
            tup = (distances[q(i,j,N_IMG)], j)
            if i == j:
                tup = (0, j)
            r.append(tup)
        r = sorted(r, key=lambda x: x[0])
        m.append(r)
    return m

def similarity_image(chosen_img, similarity_matrix, paths):
    new_img = Image.new('RGB', (995, 410), "#f8fafc")
    for i in range(10):
        im_num = similarity_matrix[chosen_img][i][1]
        path = paths[im_num]
        img = Image.open(path)
        img.thumbnail((200, 200))
        pos = ((i % 5) * 210, int(math.floor(i / 5.0) * 210))
        new_img.paste(img, pos)
        new_img.save('output/'+ str(N_IMG) + 'if' + str(chosen_img) + '.jpg')
    new_img.show()


def run():
    paths = make_paths_list()
    feats = make_feats(paths)
    similarity_image = calculate_sim(feats)

    chosen_images = sample(range(N_IMG), 3)
    for k in range(len(chosen_images)):
        chosen_img = chosen_images[k]
        similarity_image(chosen_img, similarity_rankings, paths)
run()











