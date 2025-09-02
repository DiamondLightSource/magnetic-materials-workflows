FROM quay.io/condaforge/miniforge3

# Install Python and Conda packages
RUN conda install --yes -c conda-forge \
    numpy \
    matplotlib \
    h5py \
    hdf5plugin \
    imageio \
    jupyter \
    nbconvert \
    nbformat \
    papermill \
    hdfmap \
    nexus2srs \
    && conda clean --all --yes

# Install system dependencies and clean up
RUN apt-get update && \
    apt-get install -y curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Download and extract MSMapper
RUN mkdir -p /opt/msmapper && \
    curl -L https://alfred.diamond.ac.uk/MSMapper/master/builds-snapshot/MSMapper-1.9.0.v20250205-1441-linux.x86_64.zip -o /opt/msmapper/archive.zip && \
    unzip -n /opt/msmapper/archive.zip -d /opt/msmapper && \
    rm /opt/msmapper/archive.zip
