FROM python:3.9-slim

WORKDIR /FS

COPY requirements.txt ./

COPY fibonacci_server.py ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9090

CMD ["python", "fibonacci_server.py"]