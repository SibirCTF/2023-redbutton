FROM python:3.10.12
WORKDIR /srv
RUN pip install --upgrade pip
RUN pip install flask
COPY . /srv
#ENV FLASK_APP=app
#ENTRYPOINT["python"]
EXPOSE 5000

CMD ["python","база.py", "1111","--ip_jury=192.168.0.69", "--port_jury=30555" ]
