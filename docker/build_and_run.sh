parentdir=$(dirname `pwd`)
uid=$(id -u ${USER})
gid=$(id -g ${USER})
# Include --no-cache if needing to rebuild for a test
docker build -t "unnamed_project" .

docker run --gpus all -it --rm --name unnamed_project  -p 8862:8862 -v $parentdir:/module unnamed_project /bin/bash