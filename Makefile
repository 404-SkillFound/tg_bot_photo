SRC_DIR := ./photo_bot

run:
	python3 -m uvicorn main:app --reload