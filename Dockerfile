FROM mygeotools:v1
COPY wget_files.txt wget_files.txt
# Download some NaturalEarth data for cartopy
ENV CARTOPY_DIR=/usr/local/cartopy-data
ENV NE_PHYSICAL=${CARTOPY_DIR}/shapefiles/natural_earth/physical
ENV NE_CULTURAL=${CARTOPY_DIR}/shapefiles/natural_earth/cultural
RUN mkdir -p ${NE_PHYSICAL}
RUN apt-get -yq install unzip
RUN wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_coastline.zip -P ${CARTOPY_DIR}
RUN wget -i wget_files.txt -P ${CARTOPY_DIR}
RUN unzip ${CARTOPY_DIR}/'*.zip' -d ${NE_PHYSICAL}
RUN unzip ${CARTOPY_DIR}/'*.zip' -d ${NE_CULTURAL}
RUN rm ${CARTOPY_DIR}/*.zip
COPY . /app
COPY ./data /data
CMD python /app/app.py

