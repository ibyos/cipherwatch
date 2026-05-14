FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --break-system-packages -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "app/api.py"]
