FROM python:3.12.4

WORKDIR /code

ENV environment=production

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./backend /code/app

CMD ["fastapi","run", "backend/app.py","--port","8000"]

EXPOSE 8000





