# HRS
Healthcare recommender system practice project

🇳🇱 Nederlands
Dit project is een Flask API die, op basis van een ingevoerde postcode, automatisch de vijf best passende zorglocaties teruggeeft. De ranking wordt bepaald door een gewogen combinatie van:

📍 Afstand tot de gebruiker (korter = beter)

✅ Kwaliteitsscore (IndicatorWaarde, hoger = beter)

⏳ Wachttijd (korter = beter)

De gegevens worden ingelezen uit een CSV-bestand, en de afstand wordt berekend met behulp van pgeocode. De gebruiker krijgt als output een gesorteerde lijst van matches inclusief locatiegegevens en een directe link naar Google Maps voor routeplanning.

Gebruik:
Stuur een GET-request naar /best_match?postcode=1234AB om de top 5 locaties te ontvangen op basis van postcode 1234AB.

Disclaimer:
Werkt alleen voor revalidatiecenters momenteel

🇬🇧 English
This project is a Flask API that returns the five best matching healthcare facilities based on a user-provided Dutch postal code. The ranking is determined using a weighted score that incorporates:

📍 Distance to the user (shorter = better)

✅ Quality indicator score (higher = better)

⏳ Waiting time (shorter = better)

Data is loaded from a CSV file, and distances are computed using pgeocode. The API returns a sorted list of best matches, including location details and direct Google Maps directions.

Usage:
Send a GET request to /best_match?postcode=1234AB to receive the top 5 healthcare locations ranked for postal code 1234AB.

Disclaimer:
Currently only works for rehabilitation centers
