FROM kuralabs/python3-dev:latest
ENV TZ="America/Bogota"

WORKDIR /backend
COPY requirements.txt ./

RUN apt-get update && apt-get install -y locales && \
    echo "es_ES.UTF-8 UTF-8" > /etc/locale.gen && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=es_ES.UTF-8
ENV LANG es_ES.UTF-8

# Install dependencies
RUN apt-get install -y python3-dev python3-pip build-essential
RUN apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev 
RUN apt-get install -y libsqlite3-dev liblzma-dev libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
RUN apt-get install -y libglib2.0-0
# RUN pip3 install h5py
# RUN apt-get install -y hdf5 ffmpeg build-dep setuptools python3-pip

# RUN pip3 install -r requirements.txt
RUN pip3 install setuptools==66.1.1
RUN pip3 install psutil==6.0.0 
RUN pip3 install ultralytics 
RUN pip3 install opencv-python-headless==4.10.0.84 
RUN pip3 install opencv-python==4.10.0.84 
RUN pip3 install sentence-transformers==3.0.1
RUN pip3 install gensim==4.3.2
RUN pip3 install nltk==3.8.1
RUN pip3 install sounddevice==0.4.7
RUN pip3 install -U openai-whisper
RUN pip3 install moviepy==1.0.3
RUN pip3 install boto3==1.34.150
RUN pip3 install openpyxl==3.1.5
RUN pip3 install tables

COPY project /backend/project
COPY resources /backend/resources
COPY tests /backend/tests
COPY constants.py /backend
COPY .python-version /backend
COPY yolov5n.pt /backend
COPY __init__.py /backend
RUN mkdir -p uploads/how2sign/videos

# RUN apt-get -y update && apt-get -y upgrade --fix-missing
# RUN apt-get -y install pipx
# RUN rm -Rf /app/uploads/how2sign/videos/*.mp4
WORKDIR /backend

ENV PYTHONPATH="${PYTHONPATH}/backend"
CMD ["python3", "__init__.py"]
RUN python3 resources/boostraps/corpus.py
ENTRYPOINT ["python3", "project/adapters/cli/v1/__init__.py"]
# CMD ["python3", "project/adapters/cli/v1/__init__.py", "--model", "hamodel", "--test_audio_v2", "True"]