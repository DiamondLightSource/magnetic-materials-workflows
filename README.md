# magnetic-materials-workflows
## Workflows Templates
See [workflows.diamond.ac.uk](workflows.diamond.ac.uk)

| Template                                                                                        | Description                            |
|-------------------------------------------------------------------------------------------------|----------------------------------------|
| [https://workflows.diamond.ac.uk/templates/msmapper-notebook](msmapper-notebook)                | Generate recriprocal space maps        |
| [https://workflows.diamond.ac.uk/templates/xas-notebook](xas-notebook)                          | Subtract background and calcualte XMCD |
| [https://workflows.diamond.ac.uk/templates/i21-image-processing-notebook](i21-image-processing) | Basic image processing for i21         |
| [https://workflows.diamond.ac.uk/templates/mmg-test-notebook](mmg-test-notebook)                | test notebook                          |
| [https://workflows.diamond.ac.uk/templates/mmg-test-python](mmg-test-python)                    | test script                            |


## miniconda environment
Contains a Docker image that includes:
* conda-forge miniconda python environment with:
  * numpy
  * matplotlib
  * jupyter
  * papermill
  * hdfmap
  * nexus2srs
  * mmg_toolbox

At DLS, the image can be run using, for example:
```bash
podman run -it ghcr.io/diamondlightsource/magnetic-materials-workflows /bin/bash
```

To update the Docker image, make changes to the base [Dockerfile](images/base/Dockerfile) and create a new release.