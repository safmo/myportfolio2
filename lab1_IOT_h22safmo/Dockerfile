FROM python:3.9-slim

# set a directory for the app
#WORKDIR /usr/src/app
WORKDIR /code

# copy all the local src files to the container
#COPY . .
# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the content of the local src directory to the working directory
#COPY src/ .
COPY mqtt_device1.py .

# tell the port number the container should expose
#EXPOSE 8883

# RUN echo "Hello World!"
# run the command
CMD ["python", "./mqtt_device1.py"]
