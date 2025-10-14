FROM python:3.14-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY plot-models-scatter.py /usr/local/bin/scatter-svg
RUN chmod +x /usr/local/bin/scatter-svg

ENTRYPOINT ["/usr/local/bin/scatter-svg"]
