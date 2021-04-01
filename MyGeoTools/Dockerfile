FROM purposefly/anaconda
MAINTAINER yaakov@gesher.net

RUN conda update conda
RUN conda create -n gdalenv -y python=3.6

SHELL ["/bin/bash", "-c"]
RUN source activate gdalenv

RUN conda install -y gdal
RUN conda install --yes cartopy
RUN conda install --yes geopandas
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys AA8E81B4331F7F50
RUN apt-get update
RUN apt-get install libav-tools -y
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

