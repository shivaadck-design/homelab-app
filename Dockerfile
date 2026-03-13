FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc pkg-config && rm -rf /var/lib/apt/lists/*
COPY app.py .
RUN pip install flask mysqlclient
CMD ["python", "app.py"]
