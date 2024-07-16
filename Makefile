APPLICATION_NAME ?= mostsecuredapp
VERSION ?= v1
REGISTRY ?= docker.io
USERN ?= theusername
CONTAINER_IMAGE = $(REGISTRY)/$(USERN)/$(APPLICATION_NAME)

dockerBuildLatest:
	@echo "Latest Build Started >>"
	docker build --tag $(CONTAINER_IMAGE):latest .
	@echo "Latest Build Done!"

dockerBuild:
	@echo "Build Started >>"
	$(MAKE) dockerBuildLatest
	@echo "Build Done!"

run:
	@python3 myapp.py

lintCheck:
	@( \
    	pip install pylint; \
		pylint myapp.py --fail-under 8 --fail-on E; \
	)

securityCheck:
	@( \
		pip3 install bandit; \
		bandit -r myapp.py -f json | jq '.metrics._totals'; \
		bandit -r myapp.py -f json | jq -e '.metrics._totals."SEVERITY.HIGH" == 0'; \
	)

check:
	$(MAKE) lintCheck
	$(MAKE) securityCheck