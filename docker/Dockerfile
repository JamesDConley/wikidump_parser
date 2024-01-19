################
## BASE SETUP ##
################
FROM tensorflow/tensorflow:2.6.0-gpu-jupyter
WORKDIR /installs

###############################
## INSTALL BASE DEPENDENCIES ##
###############################
COPY installation_media/requirements.txt .
COPY installation_media/install_base_deps.sh .
RUN bash install_base_deps.sh

# Move user to the mounted volume for the project
WORKDIR /module