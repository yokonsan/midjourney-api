FROM python:3.10 AS builder

COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim

WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local:$PATH

RUN chmod +x entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]
EXPOSE 8062
CMD ["http"]
