FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask gunicorn

COPY ex3-flash-sale.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "ex3-flash-sale:app"]
