# magnetic-materials-workflows
## Python Images

## miniconda environment
Contains a Docker image that includes:
* conda-forge miniconda python environment with:
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

At DLS, the image can be run using, for example:
```bash
podman run -it ghcr.io/diamondlightsource/magnetic-materials-workflows /bin/bash
```

To update the Docker image, make changes to [Dockerfile](base/Dockerfile) and create a new release.