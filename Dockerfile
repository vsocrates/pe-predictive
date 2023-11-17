FROM continuumio/anaconda3:2021.05

EXPOSE 5000 

RUN apt-get update

# Install software dependencies

RUN apt-get update
RUN apt-get -y install graphviz

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip 
RUN apt-get install python3-dev -y \
                        gcc -y \
                        libc-dev -y 

# RUN apt-get install python3-dev -y && \
# apt-get install libevent-dev -y

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Install jupyter notebook
RUN /opt/conda/bin/conda install jupyter -y --quiet 
RUN /opt/conda/bin/python -m nltk.downloader -d /usr/local/share/nltk_data all

RUN mkdir /code
RUN mkdir /data

# Add the code
ADD . /code
WORKDIR /code/pefinder

# Clean up
RUN apt-get autoremove -y
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# RUN chmod u+x /code/pefinder/cli.py

# ENTRYPOINT ["python","/code/pefinder/cli.py"]


WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD [ "python3", "-m" , "flask", "--app=deploy", "--port=5005", "run"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5005", \
# "--timeout", "120" ,\
# #  "--threads", "2", \
# # "--worker-tmp-dir", "/dev/shm",\
# "--workers", "2", "--threads", "1", "--worker-class", "async", \
#  "deploy:app"]
# CMD ["waitress-serve", "--host", "127.0.0.1", "--call", "webapp:app"]

CMD ["flask", "-A", "webapp", "run", "--host", "0.0.0.0"]