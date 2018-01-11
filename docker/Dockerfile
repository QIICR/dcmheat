FROM thewtex/centos-build:latest
#FROM fedorov/docker-centos-build:centos6

#RUN apt-get update
#RUN apt-get install --yes curl zip unzip

ADD setup_slicer.sh /usr/src/setup_slicer.sh
RUN /usr/src/setup_slicer.sh

#ADD setup_dcm2niix.sh /usr/src/setup_dcm2niix.sh
#RUN /usr/src/setup_dcm2niix.sh

## Setup tools

### dcm2niix - build from source, since binaries have issues with missing GLIBC version
###  installs to /usr/local, in the PATH

RUN cd /tmp && \
	git clone https://github.com/rordenlab/dcm2niix.git && \
	cd dcm2niix && git checkout  v1.0.20171215 && \
	mkdir build && cd build && \
	cmake -DBATCH_VERSION=ON -DINSTALL_PREFIX=/usr -DUSE_OPENJPEG=ON .. && \
	make && make install

#ENV PATH="/usr/dcm2niix:${PATH}"

## Setup data

RUN mkdir /usr/data
ADD setup_datasets.sh /usr/src/setup_datasets.sh
RUN /usr/src/setup_datasets.sh

## Get the cmake test setup
ADD test /usr/src/test
RUN mkdir /usr/dcmheat && cd /usr/dcmheat && cmake /usr/src/test
