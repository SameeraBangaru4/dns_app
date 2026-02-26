FROM python:3.9-slim

WORKDIR /AS

RUN mkdir -p /AS && chmod 777 /AS

COPY requirements.txt ./

COPY auth_server.py ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 53533

CMD ["python", "-u", "auth_server.py"]