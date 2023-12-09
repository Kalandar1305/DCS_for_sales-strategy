#Using NVCR tensorflow image with spark master & worker and jupyter notebook

FROM nvcr.io/nvidia/tensorflow:21.06-tf2-py3

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --upgrade pip

WORKDIR /workspace

COPY jupyter_notebook_config.py /root/.jupyter

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt update && \
    apt upgrade -y && \
    apt install -y default-jdk-headless openvpn ssh

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb

RUN wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin

RUN rm -rf * && \
    apt autoremove --purge

CMD ["jupyter", "notebook"]
