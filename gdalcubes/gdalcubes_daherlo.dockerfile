FROM daherlo/gdalcubes:pafyc
RUN apt-get update && apt-get install -y \
  qt5-default
COPY gdalcubes_process_data_cubes /bin
COPY gdalcubes_create_images_collections /bin
