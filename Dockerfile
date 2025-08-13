FROM quay.io/condaforge/miniforge3
RUN conda install -c conda-forge numpy matplotlib h5py hdf5plugin imageio jupyter nbconvert nbformat papermill hdfmap nexus2srs
RUN mkdir -p /opt/msmapper
RUN <<EOF
apt-get update
apt-get install -y curl unzip
EOF
RUN curl https://alfred.diamond.ac.uk/MSMapper/master/builds-snapshot/MSMapper-1.9.0.v20250205-1441-linux.x86_64.zip -o /opt/msmapper/archive.zip
RUN unzip -n /opt/msmapper/archive.zip -d /opt/msmapper
RUN rm /opt/msmapper/archive.zip
