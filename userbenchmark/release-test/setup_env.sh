#!/bin/bash

set -xeuo pipefail

CUDA_VERSION="$1"
MAGMA_VERSION="$2"
PYTORCH_VERSION="$3"
PYTORCH_CHANNEL="$4"
WORK_DIR="$5"

GPU_FREQUENCY="5001,900"
# get the directory of the current script
CURRENT_DIR=$(dirname -- "$0")

. switch-cuda.sh ${CUDA_VERSION}
# re-setup the cuda soft link
if [ -e "/usr/local/cuda" ]; then
    sudo rm /usr/local/cuda
fi
sudo ln -sf /usr/local/cuda-${CUDA_VERSION} /usr/local/cuda
conda uninstall -y pytorch torchvision torchtext pytorch-cuda
# make sure we have a clean environment without pytorch
pip uninstall -y torch torchvision
pip uninstall -y torch torchvision
pip uninstall -y torch torchvision

# install magma and pytorch-cuda/cudatoolkit
conda install -y -c pytorch ${MAGMA_VERSION}
# install pytorch and cuda toolkit
# weiwangmeta@: torchvision/torchtext not available
#conda install -y -c ${PYTORCH_CHANNEL} pytorch=${PYTORCH_VERSION} torchvision torchtext \
#                 -c conda-forge cudatoolkit=${CUDA_VERSION}
conda install -y -c ${PYTORCH_CHANNEL} pytorch=${PYTORCH_VERSION} \
                 -c conda-forge cudatoolkit=${CUDA_VERSION}
python -c 'import torch; print(torch.__version__); print(torch.version.git_version)'

# tune the machine
sudo nvidia-smi -ac "${GPU_FREQUENCY}"

pip install -U py-cpuinfo psutil distro
