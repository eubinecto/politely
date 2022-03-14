mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"tlrndk123@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

# for building khaiii
pip install cmake   # installing cmake is essential
git clone https://github.com/kakao/khaiii.git
cd khaiii || exit
mkdir build
cd build || exit
cmake .. || exit
make all resource || exit
make install || exit
make package_python || exit
cd package_python || exit
pip install . || exit
