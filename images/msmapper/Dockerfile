FROM quay.io/condaforge/miniforge3 AS build

# Install Python and Conda packages
COPY environment.yml .
RUN conda env create -f environment.yml && \
    conda install -c conda-forge conda-pack && \
    conda clean --all --yes && \
    conda-pack -n mmg_toolbox -o /tmp/env.tar && \
    mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
    rm /tmp/env.tar && \
    rm -rf /opt/conda/pkgs
 
RUN /venv/bin/conda-unpack

# Install system dependencies and clean up
RUN apt-get update && \
    apt-get install -y curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Download and extract MSMapper 
RUN mkdir -p /opt/msmapper && \
    curl -L https://alfred.diamond.ac.uk/MSMapper/master/builds-snapshot/MSMapper-1.9.0.v20250205-1441-linux.x86_64.zip -o /opt/msmapper/archive.zip && \
    unzip -n /opt/msmapper/archive.zip -d /opt/msmapper && \
    rm /opt/msmapper/archive.zip

# Second minimal image for runtime
FROM debian:buster AS runtime
 
COPY --from=build /venv /venv
COPY --from=build /opt/msmapper /opt/msmapper
 
ENV PATH="/venv/bin:$PATH"



