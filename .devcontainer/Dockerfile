ARG PYTHON_VER="3.11"

FROM python:$PYTHON_VER

ARG PYTHON_ENV=my_env

ENV PYTHON_ENV=$PYTHON_ENV

ENV TZ=America/New_York

EXPOSE 8080
EXPOSE 8051

RUN mkdir requirements

RUN pip install --upgrade pip

COPY requirements.txt set_python_env.sh /requirements/

RUN bash ./requirements/set_python_env.sh $PYTHON_ENV

# Production Streamlit Run
# streamlit run ./tests/st-vslidate.py  --server.address 127.0.0.1 --server.port 8051


