FROM python:3.13-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --no-cache-dir .

CMD ["python", "KFC_Py/chess_server.py"]