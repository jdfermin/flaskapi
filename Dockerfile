FROM python:3.9-slim-buster as build

WORKDIR /app

COPY requirements.txt ./

ENV HTTP_PROXY http://proxylab.ucab.edu.ve:3128
ENV HTTPS_PROXY http://proxylab.ucab.edu.ve:3128

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["flask","run","--host=0.0.0.0", "--port=8000"]
