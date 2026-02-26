FROM python:3.9-slim

WORKDIR /US

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY userserver.py ./

EXPOSE 8080

CMD ["python", "userserver.py"]