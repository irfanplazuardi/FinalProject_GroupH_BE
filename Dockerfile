FROM python:3.9

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

ENV FLASK_APP=index.py
ENV FLASK_ENV=production


EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]



