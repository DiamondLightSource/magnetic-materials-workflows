# magnetic-materials-workflows
## Python Images

This repository contains a number of pre-built images for running workflows and other tasks.

You can pull and run the images using Docker or Podman, for example:
```bash
podman pull ghcr.io/diamondlightsource/magnetic-materials-workflows:latest
podman run -it ghcr.io/diamondlightsource/magnetic-materials-workflows:latest /bin/bash
```
The second command starts a bash prompt where you can start python or investigate the image container.

## Available images

| Name     | Description                                                                  | tag                                                                     |
|----------|------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| base     | Just the python environment, no additional software                          | ghcr.io/diamondlightsource/magnetic-materials-workflows:latest          |
| msmapper | also includes msmapper for re-mapping of detector data into reciprocal space | ghcr.io/diamondlightsource/magnetic-materials-workflows/msmapper:latest |
| quanty   | also includes the Quanty package for XAS and XMCD calculations               | ghcr.io/diamondlightsource/magnetic-materials-workflows/quanty:latest   |

## miniconda environment
Each image contains a python environment that includes the following packages:
  * numpy
  * matplotlib
  * pyvista
  * plotly
  * marimo
  * pandas
  * jupyter
  * papermill
  * hdfmap
  * nexus2srs
  * mmg_toolbox


## Updating the images
To update the Docker images, make changes to [Dockerfile](base/Dockerfile) and create a new release.

The Quanty image must be updated manually.