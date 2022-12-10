FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# CMD panel serve  --port=5006 main.py
CMD python /app2/main.py

