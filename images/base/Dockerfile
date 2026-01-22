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

# Second minimal image for runtime
FROM debian:buster AS runtime
 
COPY --from=build /venv /venv
 
ENV PATH="/venv/bin:$PATH"



