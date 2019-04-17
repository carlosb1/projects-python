FROM ubuntu:xenial

# Building in the docker image increases the size because all the deps are installed
# if these are done in separate RUN commands they get put into diff. layers and removing later has no effect apparently
# as a result, all build/remove commands are pushed into one RUN command, the docker image goes from 808 MB to 300 by doing so
# EXPOSE 8080
# EXPOSE 5002
ADD . /code
RUN apt-get -y update && \
    apt-get install -y python-pip wget curl && \
    cd ~ && \
    curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh && \
    chmod +x nodesource_setup.sh && \
    ./nodesource_setup.sh && \
    apt-get install -y nodejs && \
    cd /code && \
    rm -rf frontend/node_modules && \
    cd frontend && npm install && cd .. && \
    pip install -r requirements.txt    
CMD ./run.sh
CMD while true; do sleep 1000; done;
