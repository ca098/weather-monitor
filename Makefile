dev_export:
	export $(cat local.env | xargs)

run_tests: dev_export
	pytest

