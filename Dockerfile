FROM python:3.9
RUN git clone https://github.com/soymadip/Auto-forward-bot
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
