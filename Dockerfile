# Create an image for our restAPI following these requirements
#FROM ubuntu:latest
FROM python:3.12
LABEL authors="gallas"
#ENTRYPOINT ["top", "-b"]
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# run : docker build -t store-restapi .
# /app is a conventional path for app data.
# Containers share the host's OS kernel, eliminating the need for a separate OS.
# Cached layers reduce build time by avoiding redundant steps.

# run : docker run -d -p 5005:5000 -w /app -v "%cd%:/app" store-restapi
# To mount the current directory s that you won't have rebuild after every change
# Only for development env !!!