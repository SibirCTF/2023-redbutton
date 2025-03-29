FROM pwntools/pwntools:stable

WORKDIR /app

COPY . /app

ENTRYPOINT [ "python" ]
EXPOSE 4444

CMD ["lenin.py", "1111","--ip_jury=192.168.0.69", "--port_jury=30555" ]
