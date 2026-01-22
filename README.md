# magnetic-materials-workflows

This repository contains workflow templates and Docker images for use in Diamond's 
argus-workflows data analysis platform.

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
Contains several Docker images that includes a python environment and other useful software. 
The python environment includes:
* conda-forge miniconda python environment with:
  * numpy
  * matplotlib
  * jupyter
  * papermill
  * hdfmap
  * nexus2srs
  * mmg_toolbox
