.PHONY: run-dev
run-dev:
	uvicorn src.main:app --port 8080 --reload