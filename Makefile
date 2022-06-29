
demo:
	python3 main_demo.py

local:
	streamlit run main_streamlit.py

test:
	pytest

format:
	black ./ --line-length=110