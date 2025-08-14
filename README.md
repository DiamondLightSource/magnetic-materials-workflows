# magnetic-materials-workflows
## Workflows Template
See [workflows.diamond.ac.uk](workflows.diamond.ac.uk)

Contains a Docker image that includes:
* conda-forge miniconda python environment with:
  * numpy
  * matplotlib
  * jupyter
  * papermill
  * hdfmap
  * nexus2srs
* msmapper

At DLS, the image can be run using, for example:
```bash
podman run -it ghcr.io/diamondlightsource/magnetic-materials-workflows:0.2.0-rc1 /bin/bash
```

To update the Docker image, make changes to [Dockerfile](Dockerfile) and create a new release.