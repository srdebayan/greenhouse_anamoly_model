FROM python:3.9
 
ADD analyzer.py .

EXPOSE 8086

RUN pip install paho-mqtt 
RUN pip install influxdb-client
RUN pip install numpy
RUN pip install -U scikit-learn
 
CMD [ "python", "./analyzer.py" ]
