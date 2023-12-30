.phony: scrap update

update:
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

scrap:
	python -m mtgdc_scrapper

card-data:
	python -m mtgdc_carddata