# https://github.com/potree/PotreeConverter/issues/281#issuecomment-335471817
FROM python:3.9
EXPOSE 8501
WORKDIR /politetune
# install python libs
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
# install khaiii
RUN git clone https://github.com/kakao/khaiii.git
RUN mkdir /politetune/khaiii/build || exit
WORKDIR /politetune/khaiii/build
RUN cmake -E env CXXFLAGS="-w" cmake .. || exit
RUN make all resource || exit
RUN make install || exit
RUN make package_python || exit
RUN pip install package_python/. || exit
# then deploy
WORKDIR /politetune
COPY . .
# https://github.com/gliderlabs/docker-alpine/issues/144
RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LC_ALL ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
CMD streamlit run --server.port $PORT main_deploy.py
