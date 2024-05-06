FROM python:3.9
 
ADD analyzer.py .
 
RUN pip install paho-mqtt 
RUN pip install influxdb-client
 
CMD [ "python", "./analyzer.py" ]