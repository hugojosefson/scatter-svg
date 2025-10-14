FROM python:3.11-slim

RUN pip install --no-cache-dir matplotlib adjustText pandas

COPY plot-models-scatter.py /usr/local/bin/scatter-svg
RUN chmod +x /usr/local/bin/scatter-svg

ENTRYPOINT ["/usr/local/bin/scatter-svg"]
