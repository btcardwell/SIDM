from dask.distributed import print
import dask
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
print("__init__ time! BASE_DIR: {BASE_DIR}")