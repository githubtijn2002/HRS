from flask import Flask, request, jsonify
import pandas as pd
import pgeocode


# Load data
df = pd.read_csv('WaitingTimes_2.csv', sep=',', encoding='utf-8')
df['Postcode_kort'] = df['Postcode_kort'].astype(str).str[:4]  # Make sure it's string
app = Flask(__name__)
geo = pgeocode.GeoDistance('NL')

@app.route('/best_match', methods=['GET'])
def best_match():
    # Get postcode from query parameter
    postcode = request.args.get('postcode')
    if not postcode:
        return jsonify({'error': 'No postcode provided'}), 400

    try:
        postcode_short = int(str(postcode)[:4])
    except ValueError:
        return jsonify({'error': 'Invalid postcode'}), 400

    # Compute distances to all locations
    distances = df['Postcode_kort'].apply(lambda x: geo.query_postal_code(str(postcode_short), str(x)))
    distanceval = ((distances - distances.min()) / (distances.max() - distances.min()))
    waittime = df['WaitingTime'] * 1.5
    waittime = (waittime - waittime.min()) / (waittime.max() - waittime.min())

    score1 = -((distanceval + 1)**2)
    score2 = (df['IndicatorWaarde']/10)**2
    score3 = -((waittime + 1)**2)
    total_score = score1 + score2 + score3
    total_score = (total_score - total_score.min()) / (total_score.max() - total_score.min())

    top5_indices = total_score.nlargest(5).index
    matches = []

    for rank, i in enumerate(top5_indices, start=1):
        match = {
            '% match': float(total_score[i]*100),
            'Rank': int(rank),
            'OrganisatieNaam': str(df.iloc[i]['LocatieNaam']),
            'Postcode': str(df.iloc[i]['LocatiePostcode']),
            'Plaats': str(df.iloc[i]['LocatiePlaats']),
            'Kwaliteit': float(df.iloc[i]['IndicatorWaarde']),
            'WaitingTime [Days]': float(df.iloc[i]['WaitingTime']),
            'Distance [KM]': float(round(distances[i], 2)),
            'GoogleMapsLink': f"https://www.google.com/maps/dir/?api=1&origin={postcode}&destination={df.iloc[i]['LocatiePostcode']}"
        }
        matches.append(match)


    return jsonify(matches), 200
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
