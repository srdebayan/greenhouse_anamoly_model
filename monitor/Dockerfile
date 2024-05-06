FROM python:3.9
 
ADD monitor.py .
 
RUN pip install paho-mqtt 
RUN pip install influxdb-client
 
CMD [ "python", "./monitor.py" ]