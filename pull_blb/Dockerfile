FROM python:3.7-slim AS compile-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

COPY ./pull_mult_p.py /app/
# RUN mkdir /vid
RUN pip install --user azure-storage-blob==12.1.0
RUN pip install --user tqdm

FROM python:3.7-slim AS build-image
COPY --from=compile-image /root/.local /root/.local
COPY --from=compile-image /app /app

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH
WORKDIR /app
# ENTRYPOINT ["python", "pull_mult_p.py"]

