FROM python:3.9
 
ADD executor.py .
 
RUN pip install paho-mqtt 
RUN pip install numpy
 
CMD [ "python", "./executor.py" ]
