from flask import Flask, request, render_template, redirect, url_for
import json
import requests
import base64
import uuid

app = Flask(__name__)

# Sample questions
questions = [
    {"id": 1, "question": "What is your full name?"},
    {"id": 2, "question": "What is your email address?"},
    {"id": 3, "question": "What is your phone number?"},
    {"id": 4, "question": "Which company do you work for?"},
    {"id": 5, "question": "What Apache project is the de facto standard for data streaming?"},
    {"id": 6, "question": "What year was Confluent established?"},
    {"id": 7, "question": "Who is the founder of Apache Kafka, who also serves as the CEO of Confluent?"},
    {"id": 8, "question": "What is the name of the real-time streaming SQL engine for Apache Kafka?"}
]


# This URL would be the endpoint where answers are submitted
# This URL would be the endpoint where answers are submitted
SUBMISSION_URL = "https://pkc-12576z.us-west2.gcp.confluent.cloud:443/kafka/v3/clusters/lkc-51m5gq/topics/submitted_answers/records"
SUBMISSION_URL_KSQLDB = "https://pksqlc-k8mj5p.us-west2.gcp.confluent.cloud/query"
AUTH_HEADER = "TlpXUVRFTUNNWEVFV1dSVjpwWkRhL3JGU25mTmWE5c2rSCtiRVJ1N1FvbTNobzFJ"
AUTH_HEADER_KSQLDB = "WklBRVVSM0g0UzRXTlJOUjpHSUVGS85SVVQS0h0dnhLaVFxMEExcERPWnlJdzFQ"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {AUTH_HEADER}"
}

headers_ksqldb = {
    "Authorization": f"Basic {AUTH_HEADER_KSQLDB}",
    "Accept": "application/vnd.ksql.v1+json",
    "Content-Type": "application/json"
    }

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/checkresult')
def checkresult():
    return render_template('checkresult.html')

@app.route('/results', methods=['GET'])
def results():

    data = {
        "ksql": "select * from EVALUATED_ANSWERS_Q1;",
        "streamProperties": {}
        }

    try:
        response = requests.post(SUBMISSION_URL_KSQLDB, headers=headers_ksqldb, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        external_results = response.json()

        # Extract rows and order by TOTAL_SCORE descending
        rows = [item['row']['columns'] for item in external_results if 'row' in item]
        sorted_rows = sorted(rows, key=lambda x: x[-1], reverse=True)

        # Render results in HTML
        #return render_template('results.html', sorted_rows=sorted_rows)
        columns_to_keep = [3, -1]  # Adjust these indices based on the actual positions of the columns

        # Create a new list with only the desired columns
        filtered_sorted_rows = [[row[i] for i in columns_to_keep] for row in sorted_rows]

        # Render results in HTML
        return render_template('results.html', sorted_rows=filtered_sorted_rows)


    except requests.RequestException as e:
        # Handle any errors during the API call
        return jsonify({"error": str(e)}), 500


@app.route('/submit', methods=['POST'])
def submit():
    answers = {}
    for question in questions:
        question_id = str(question['id'])
        answer = request.form.get(f"answer_{question_id}")
        if answer:
            answers[question_id] = answer

    unique_request_id = str(uuid.uuid4())
    # Convert answers dictionary to JSON
    data = {
        "value": {
            "type": "JSON",
            "data": {
                "quiz_id": 1,
                "req_id": unique_request_id,
                **answers
            }
        }
    }


    answers_json = json.dumps(data)
    print("Submitted answers in JSON format:", answers_json)


    # Send the JSON data using requests.post
    response = requests.post(SUBMISSION_URL, headers=headers, data=answers_json)

    # Print the response from the server
    print("Response from submission URL:", response.status_code, response.text)

    # Redirect to a thank you page or back to the home page
    return redirect(url_for('checkresult'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
