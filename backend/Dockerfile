FROM pytorch/pytorch:latest

RUN apt-get update && apt-get install -y libpq5 gcc libpq-dev
COPY ./backend/requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir 0 --upgrade -r /root/requirements.txt
WORKDIR /root/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]