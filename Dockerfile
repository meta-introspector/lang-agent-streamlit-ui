
FROM h4ckermike/lang_agent:dev
#FROM h4ckermike/unimath-coq-trace-batch2:test1
FROM h4ckermike/meta-coq-utils-data-1:2024-02-12

FROM python:3.8.9

# lang agent
COPY --from=0 /home/opam/ /home/opam/
COPY --from=0 /lang_agent/ /lang_agent/


COPY --from=1 /data /data 

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./packages.txt /app/packages.txt

RUN apt-get update && xargs -r -a /app/packages.txt apt-get install -y && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# User
#RUN useradd -m -u 1000 user
#RUN chmod -R 777 /data
#USER user
ENV HOME /root
ENV PATH $HOME/.local/bin:$PATH

WORKDIR $HOME
RUN mkdir app
WORKDIR $HOME/app
COPY . $HOME/app


EXPOSE 8501
CMD streamlit run app.py \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.fileWatcherType none
