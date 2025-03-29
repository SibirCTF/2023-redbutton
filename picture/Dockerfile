# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
#COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install flask
#RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]
EXPOSE 5000

CMD ["main.py", "1111","--ip_jury=192.168.0.69", "--port_jury=30555" ]
