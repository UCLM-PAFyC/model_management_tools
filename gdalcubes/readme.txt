url tutorial: http://94.23.83.201/redmine/projects/ticpa/wiki/GDALCUBES_PAFYC_DOCKERFILE

0. Install docker

1. Create text file: gdalcubes_dhl.dockerfile
   Content:
FROM appelmar/gdalcubes_service
RUN apt-get update && apt-get install -y \
  qt5-default
COPY gdalcubes_process_data_cubes /bin
COPY gdalcubes_create_images_collections /bin

2. Copy excutable files:
   gdalcubes_process_data_cubes
   gdalcubes_create_images_collections
   in gdalcubes_dhl.dockerfile directory
 
3. Open powershell in gdalcubes_dhl.dockerfile directory and create docker image:
docker build -t appelmar/gdalcubes:dhl_qt5_v3 -f gdalcubes_dhl.dockerfile .
en mi dell tarda 143 segundos

4. Commands execution examples:
docker run --rm --env PROJ_LIB=/usr/share/proj --env GDAL_DATA=/usr/share/gdal --mount type=bind,source=D:/GDALCubesProjects,target=/home appelmar/gdalcubes:dhl_qt5_v3 /bin/gdalcubes_create_images_collections /home/AmalTunez/gdalcubes/s1_vv/temp/gdalCubes_createImageCollections.txt
docker run --rm --env PROJ_LIB=/usr/share/proj --env GDAL_DATA=/usr/share/gdal --mount type=bind,source=D:/GDALCubesProjects,target=/home appelmar/gdalcubes:dhl_qt5_v3 /bin/bash -c "/bin/gdalcubes_process_data_cubes /home/AmalTunez/gdalcubes/s1_vv/temp/gdalCubes_processDataCube_docker.txt 4; sh /GcExport.sh" 