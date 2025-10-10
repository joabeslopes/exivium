FROM python:3.11-bookworm

RUN apt update && apt install ffmpeg libx264-dev git -y

WORKDIR /exivium

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]