FROM eclipse-mosquitto
 
# Copy the modified mosquitto.conf file into the container
COPY mosquitto.conf /etc/mosquitto/mosquitto.conf
 
 
EXPOSE 1883
 
# Run the Mosquitto MQTT broker with the modified configuration file
CMD ["mosquitto", "-c", "/etc/mosquitto/mosquitto.conf"]