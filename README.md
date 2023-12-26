# barrins-data
Barrin's Data is a project to analyze and predict Duel Commander (MTGDC) format:
- `mtgdc_scrapper` extracts data from [MTGTOP8](https://mtgtop8.com/index);
- `mtgdc_decklists` stores tournaments in the form of JSON files;
- `mtgdc_carddata` queries MTGJSON and builds a dictionnary of cards;
- `mtgdc_banlist` keeps track of what's legal and what's not;
- `mtgdc_clustering` reduces data to be able to analyze it easily;
- `mtgdc_aggregator` reduces a set of lists to a most probable list;
