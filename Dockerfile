# build
FROM python:3.13-slim AS build 

WORKDIR /app 

# deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# source code
COPY app ./app 
COPY content ./content 
COPY static ./static 

# port
EXPOSE 8000

# command to run app 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
