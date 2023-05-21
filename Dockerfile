FROM python:3.10.6
LABEL creator="yokon" email="944682328@qq.com"

WORKDIR /app

COPY . .
RUN pip install --upgrade pip \
    && pip install -i https://pypi.douban.com/simple/ -r requirements.txt \
    && chmod +x entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]
EXPOSE 8062
CMD ["http"]