import dask
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
dask.distributed.print("Hello from worker!")
dask.distributed.print(BASE_DIR)