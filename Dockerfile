FROM docker.io/continuumio/miniconda3:24.5.0-0
RUN conda install numpy matplotlib h5py
RUN python -m pip install git+https://github.com/DanPorter/babelscan.git
