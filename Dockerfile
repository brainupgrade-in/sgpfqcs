
FROM python:3.11-slim
WORKDIR /app
RUN mkdir -p /data
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
