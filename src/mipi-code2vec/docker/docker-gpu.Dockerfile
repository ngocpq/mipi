FROM tensorflow/tensorflow:2.0.0-gpu-py3
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN add-apt-repository -y ppa:git-core/ppa
RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    byobu \
    ca-certificates \
    git-core git \
    htop \
    libglib2.0-0 \
    libjpeg-dev \
    libpng-dev \
    libxext6 \
    libsm6 \
    libxrender1 \
    libcupti-dev \
    openssh-server \
    python3.6 \
    python3.6-dev \
    software-properties-common \
    vim \
    unzip \
    && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

RUN apt-get -y update

#  Setup Python 3.6 (Need for other dependencies)
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
RUN apt-get install -y python3-setuptools
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN pip install --upgrade pip

# Pin TF Version on v1.12.0
#RUN pip --no-cache-dir install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.12.0-cp36-cp36m-linux_x86_64.whl

# Other python packages
RUN pip --no-cache-dir install --upgrade \
	tensorflow==2.0.0\
	websockets==9.1\
	nltk~=3.5\
	numpy~=1.19.5\
	scipy~=1.5.4\
	gensim~=3.8.3\
	torch~=1.7.1\
	transformers~=4.2.2\
	docopt==0.6.2 \
    jupyter

ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# Install JDK

RUN apt-get install openjdk-8-jdk

# Open Ports for TensorBoard, Jupyter, SSH, and MIPI Websocket server
EXPOSE 6006
EXPOSE 7654
EXPOSE 22

EXPOSE 8765

WORKDIR /app/src

CMD bash
