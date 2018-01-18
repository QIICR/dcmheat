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
	cmake -DBATCH_VERSION=ON -DCMAKE_INSTALL_PREFIX=/usr -DUSE_OPENJPEG=ON .. && \
	make && make install

### plastimatch
RUN cd /tmp && \
	git clone https://gitlab.com/plastimatch/plastimatch.git && \
	cd plastimatch && git checkout v1.7.0 && \
	mkdir build && cd build && \
	cmake -DINSTALL_PREFIX=/usr .. && \
	make && make install && \
	cp plastimatch /usr/bin

### FreeSurfer
### This one is 4.5Gb!
#RUN curl -c -v -L ftp://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/6.0.0/freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.0.tar.gz | tar xz -C /usr/

#ENV PATH="/usr/dcm2niix:${PATH}"

ADD get-pip.py /usr/src/get-pip.py
RUN cd /usr/src && python get-pip.py && python get-pip.py && pip install dicom2nifti

## Setup data
RUN mkdir /usr/data 
RUN curl -c -v -o /usr/data/dcmheat.zip -L https://www.dropbox.com/s/h75cttxculzcvbt/dcmheat.zip?dl=1
RUN cd /usr/data && unzip dcmheat.zip && rm dcmheat.zip

## Run the tests
ADD tester.py /usr/src/tester.py
RUN python /usr/src/tester.py -i /usr/data/dcmheat -o /usr/data/dcmheat

## this helps looking at the results
RUN yum install -y tree
