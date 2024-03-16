.PHONY: run-dev
run-dev:
	uvicorn src.main:app --reload