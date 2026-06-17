#!/bin/bash

docker run -d --rm --name busybox busybox:musl sleep 100

docker cp $(docker ps -ql):/bin/busybox ./

chmod +x busybox
