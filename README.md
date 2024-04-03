# EmoRoBERTa Sentiment Analysis API

This repository contains a Flask API that uses the EmoRoBERTa model to perform sentiment analysis on a list of phrases. The API accepts a CSV file with a column named "phrase" and returns the sentiment analysis results for each phrase, along with a summary table and a chart visualizing the emotion distribution. The project also includes a frontend that allows users to interact with the API through a web interface.

## Getting Started

To get started with this API, follow these steps:

1. Clone this repository to your local machine:
```
git clone https://github.com/Johnniewhite/sentiment-analysis.git
```
2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate (Linux)
venv\Scripts\activate (Windows)
```
3. Install the required packages:
```
pip install -r requirements.txt
```
4. Run the API:
```
python index.py
```
The API will be available at `http://0.0.0.0:8000`.

5. Open the frontend:
```
Open index.html in a web browser
```
The frontend will be available at `http://localhost`.

## API Endpoint

The API has one endpoint: `/analyze_sentiment_csv`. This endpoint accepts a POST request with a CSV file attached as a form-data field named "file". The CSV file should have a column named "phrase" containing the phrases to be analyzed.

The endpoint returns a JSON response containing the following fields:

* `emotion_labels`: A list of dictionaries, where each dictionary contains the sentiment analysis result for a single phrase. Each dictionary has the following keys:
	+ `label`: The predicted emotion label (e.g., "happy", "sad", "angry", etc.).
	+ `score`: The confidence score for the predicted label.
* `summary_table`: An HTML table summarizing the sentiment analysis results for all phrases.
* `chart_img`: A base64-encoded PNG image of a chart visualizing the emotion distribution.

## Example Request

Here's an example of how to make a request to the API using the `requests` library:
```python
import requests

url = "http://0.0.0.0:8000/analyze_sentiment_csv"
csv_file = open("phrases.csv", "rb")
response = requests.post(url, files={"file": csv_file})

if response.ok:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code} {response.text}")
```
## Example Response

Here's an example of the response returned by the API:
```json
{
  "emotion_labels": [
    {"label": "happy", "score": 0.9998},
    {"label": "sad", "score": 0.9987},
    {"label": "angry", "score": 0.9976},
    ...
  ],
  "summary_table": "<table border=\"1\" class=\"dataframe\">\n<thead>\n  <tr style=\"text-align: right;\">\n    <th></th>\n    <th>count</th>\n    <th>mean</th>\n    <th>std</th>\n    <th>min</th>\n    <th>25%</th>\n    <th>50%</th>\n    <th>75%</th>\n    <th>max</th>\n  </tr>\n</thead>\n<tbody>\n  <tr>\n    <th>emotion</th>\n    <td>100</td>\n    <td>0.998762</td>\n    <td>0.001035</td>\n    <td>0.996500</td>\n    <td>0.998550</td>\n    <td>0.999000</td>\n    <td>0.999500</td>\n    <td>0.999900</td>\n  </tr>\n</tbody>\n</table>",
  "chart_img": "iVBORw0KGgoAAAANSUhEUgAAAZAAAADACAYAAADDPmKZAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz\nAAALEgAACxIB0t1+/AAAIABJREFUeJzt3X+0ZWV93/H3xxnAVIlAGJCIOpi
```
## Folder Structure
```markdown
├── README.md
├── index.html
├── index.py
├── requirements.txt
├── test_docs
└── venv
```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.