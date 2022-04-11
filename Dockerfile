# https://github.com/potree/PotreeConverter/issues/281#issuecomment-335471817
FROM python:3.9
EXPOSE 8501
WORKDIR /kps
# install python libs
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
# install khaiii
# Note: do not attmept to do this locally if your OS is not a Linux.
RUN pip3 install git+https://github.com/eubinecto/khaiii-0.4
# then deploy
WORKDIR /kps
COPY . .
# https://github.com/gliderlabs/docker-alpine/issues/144
RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LC_ALL ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
CMD streamlit run --server.port $PORT main_deploy.py
