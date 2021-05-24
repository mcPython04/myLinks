.PHONY: help test compose

# full path for this Makefile
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.DEFAULT: help

help: 
	@echo 
	@echo "make test"
	@echo "	::: Creates docker containers for application and runs tests"
	@echo "make compose"
	@echo "	::: Runs the application using docker-compose up" 
	@echo

test: 
	docker-compose -f docker-compose-test.yml up --exit-code-from web --force-recreate --build ;

compose: 
	docker-compose up -d --force-recreate --build ;  
