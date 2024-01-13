.phony: scrap update card-data banlist

update:
	pip install --upgrade pip
	pip install --upgrade --upgrade-strategy eager -r requirements.txt

scrap:
	python -m mtgdc_scrapper

card-data:
	python -m mtgdc_carddata

banlist:
	python -m mtgdc_banlist --compile-html -o output/banlist.html
