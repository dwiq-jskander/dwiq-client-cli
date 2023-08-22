# DWIQ Client CLI Tool

Code for data query / analysis available to most DWIQ staff

## Getting Started

### Prerequisites

- [VS Code](https://code.visualstudio.com/docs/setup/mac)
- [VS Code / Enable Recommended Extensions](https://code.visualstudio.com/docs/editor/extension-marketplace)
- [Docker](https://docs.docker.com/engine/install/)
- [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
If you have conda installed, but `conda activate dwiq-client-cli` fails with `conda not found`, use the helper script via `source conda.sh` before running other make commands
- [Make](https://formulae.brew.sh/formula/make)

### Setup Local Environment

#### Python

```shell
# Creates the Python Environment
make init

# Use the environment (add to your .zshrc file to initialize upon startup)
conda activate dwiq-client-cli

# Add Python Libs to the Local Env
make install
```

#Python

