FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app 

WORKDIR /app
COPY data_layer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY data_layer data_layer


EXPOSE 8000

CMD ["uvicorn", "data_layer.main:app", "--host", "0.0.0.0", "--port", "8000"]

