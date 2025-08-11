FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Install system dependencies for Python packages
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y \
        build-essential \
        python3-venv \
        python3-dev \
        gfortran \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspaces/PrismHire

# Copy requirements file
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir \
        numpy==1.23.5 \
        pandas==1.5.3 \
        matplotlib==3.7.1 \
        seaborn==0.12.2 \
        scipy==1.10.1 \
        jupyterlab==3.6.3 \
        ipykernel==6.23.2 \
        tensorflow==2.12.0 \
        keras==2.12.0 \
        requests==2.31.0 \
        beautifulsoup4==4.12.2 \
        lxml==4.9.3 \
        Pillow==9.4.0 \
        opencv-python==4.8.1.78
