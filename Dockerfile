FROM python:3.11-bullseye

WORKDIR /main_app

COPY . /main_app

RUN pip install -r requirements.txt

CMD ["python",  "/main_app/main.py"]
