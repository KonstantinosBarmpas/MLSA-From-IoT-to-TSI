FROM python:3

ADD docker_script.py /

RUN pip3 install azure-storage-blob
RUN pip3 install azure-functions
RUN pip3 install azure-storage-blob
RUN pip3 install azure-storage-file-share
RUN pip3 install numpy
RUN pip3 install asyncio
RUN pip3 install nest-asyncio
RUN pip3 install azure-eventhub

ADD . /data /
CMD [ "python", "./docker_script.py" ]