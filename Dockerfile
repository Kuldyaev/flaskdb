FROM python:3.6

RUN mkdir -p /usr/src/orm/
WORKDIR /usr/src/orm/

COPY . /usr/src/orm/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "api.py"]
