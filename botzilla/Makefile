.PHONY: run set-webhook test bundle

run:
	python app.py

set-webhook:
	PUBLIC_URL=$(PUBLIC_URL) BOT_TOKEN=$$BOT_TOKEN python scripts/set_webhook.py

test:
	pytest -q

# Create a zip of the repo (no git needed)
bundle:
	zip -r botzilla-m1-mongo.zip \
	  app.py handlers storage scripts tests docs README.md requirements.txt .env.example Makefile
