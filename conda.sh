#!/bin/zsh

# Check if the system-wide Conda installation is available
if command -v conda &> /dev/null; then
    __conda_setup="$$(conda 'shell.zsh' 'hook' 2> /dev/null)"; \
    if [ $$? -eq 0 ]; then \
        eval "$$__conda_setup"; \
    else
        . "$$(conda info --base)/etc/profile.d/conda.sh"
    fi
elif [ -f "${HOME}/miniconda3/etc/profile.d/conda.sh" ]; then
    # Use user-specific Conda installation
    . "${HOME}/miniconda3/etc/profile.d/conda.sh"
else
    echo "Conda not found. Please install Conda and set up the environment."
    exit 1
fi
