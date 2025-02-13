FROM docker.io/continuumio/miniconda3:24.5.0-0
RUN conda install -c conda-forge numpy matplotlib h5py hdf5plugin imageio jupyter nbconvert nbformat papermill
RUN python -m pip install hdfmap nexus2srs
