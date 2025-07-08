
#!/usr/bin/env bash
mkdir -p $(pwd)/data
docker build -t prospect2sales .
docker run -p 5000:5000 \
    -v $(pwd)/data:/data \
    prospect2sales
