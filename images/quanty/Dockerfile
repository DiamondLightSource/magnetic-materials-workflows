FROM quay.io/condaforge/miniforge3 AS build

# --- Build stage: create the Python/Conda environment ---
COPY environment.yml .
RUN conda env create -f environment.yml && \
    conda install -c conda-forge conda-pack && \
    conda clean --all --yes && \
    conda-pack -n mmg_toolbox -o /tmp/env.tar && \
    mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
    rm /tmp/env.tar && \
    rm -rf /opt/conda/pkgs

RUN /venv/bin/conda-unpack

# ---- Minimal runtime image ----
FROM debian:bookworm AS runtime

# Bring in only the ready-to-use Python env
COPY --from=build /venv /venv
ENV PATH="/venv/bin:$PATH"

# We need `unzip` and CA certs to unpack the Quanty ZIP in the next step.
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates unzip && \
    rm -rf /var/lib/apt/lists/*

# --- Install Quanty from the ZIP provided as a BuildKit secret ---
# Why a secret for the ZIP (even though it doesn't contain your credentials)?
# 1) The ZIP never enters the build context or layers, so you avoid:
#    - accidental redistribution in caches or history
#    - licensing/compliance concerns from bundling vendor archives
# 2) Only the final executable is committed to the layer, keeping the SBOM clean.
# 3) If a maintainer adds debugging commands later, the ZIP path won't leak in logs/layers.
# We expect the Linux download to be a .zip containing a single file named "Quanty".
# Quanty is distributed as a precompiled binary; installation is simply copying it into PATH. [3](https://www.quanty.org/documentation/getting_started)[4](https://www.quanty.org/documentation/install)
RUN --mount=type=secret,id=quanty_zip \
    set -eu; \
    Z="/run/secrets/quanty_zip"; \
    mkdir -p /tmp/quanty && \
    unzip -q "$Z" -d /tmp/quanty && \
    # Guardrail: verify the expected content is present \
    if [ ! -f /tmp/quanty/Quanty ]; then \
        echo "Quanty executable not found in ZIP"; exit 1; \
    fi && \
    # Install the single executable to PATH \
    install -m 0755 /tmp/quanty/Quanty /usr/local/bin/Quanty && \
    rm -rf /tmp/quanty


