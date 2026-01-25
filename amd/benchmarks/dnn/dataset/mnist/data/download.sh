#!/bin/bash

BASE_URL="https://raw.githubusercontent.com/golbin/TensorFlow-MNIST/master/mnist/data"

wget "$BASE_URL/train-images-idx3-ubyte.gz"  -O train-images-idx3-ubyte.gz
wget "$BASE_URL/train-labels-idx1-ubyte.gz"  -O train-labels-idx1-ubyte.gz
wget "$BASE_URL/t10k-images-idx3-ubyte.gz"   -O t10k-images-idx3-ubyte.gz
wget "$BASE_URL/t10k-labels-idx1-ubyte.gz"   -O t10k-labels-idx1-ubyte.gz