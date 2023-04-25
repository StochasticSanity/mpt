PROJECT_NAME=poc-server
.DEFAULT_GOAL := run

.PHONY: build
build:
	go build -o poc-server main.go

.PHONY: run
run: build
	./poc-server

.PHONY: clean
clean:
	rm -f poc-server
