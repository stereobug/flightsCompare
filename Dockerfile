FROM stereodocker/flybastard
#RUN mkdir /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
# RUN python3.7 -m pip install selenium==3.141.0 tabulate==0.8.3 psycopg2-binary==2.8.3
COPY . /code/