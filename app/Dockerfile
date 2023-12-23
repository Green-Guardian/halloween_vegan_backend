FROM python:3.10-slim

WORKDIR /halloween_vegan_backend

ENV PYTHONPATH /halloween_vegan_backend
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app

RUN chmod +x app/entrypoint.sh

CMD ["app/entrypoint.sh"]