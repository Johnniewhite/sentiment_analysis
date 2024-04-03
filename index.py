import transformers
from flask import Flask, request, jsonify
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
from flask_cors import CORS
import pandas as pd
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)
CORS(app)

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoROBERTa")
emotion = pipeline("sentiment-analysis", model="arpanghoshal/EmoROBERTa")

def analyze_sentiment_for_phrases(phrases):
    emotion_labels = emotion(phrases)
    return emotion_labels

@app.route("/analyze_sentiment_csv", methods=["POST"])
def analyze_sentiment_csv():
    try:
        file = request.files['file']
        if file:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(io.BytesIO(file.read()))

            # Check if the expected column "phrase" is present in the DataFrame
            if "phrase" not in df.columns:
                return jsonify({"error": "Column 'phrase' not found in the CSV file. Please check the file format."}), 400

            phrases = df["phrase"].astype(str).tolist()

            # Analyze sentiment for the list of phrases
            emotion_labels = analyze_sentiment_for_phrases(phrases)

            # Calculate emotion_counts
            emotion_counts = pd.Series([label['label'] for label in emotion_labels]).value_counts()

            # Perform data visualization and return results
            summary_table = pd.DataFrame(emotion_labels, columns=['emotion']).describe().to_html()
            chart_img = generate_chart(emotion_counts)

            return jsonify({
                "emotion_labels": emotion_labels,
                "summary_table": summary_table,
                "chart_img": chart_img,
            })
        else:
            return jsonify({"error": "No file provided"}), 400

    except Exception as e:
        return jsonify({"error": f"Error processing the CSV file: {str(e)}"}), 500

def generate_chart(emotion_counts):
    import matplotlib.pyplot as plt
    from io import BytesIO

    # Create a bar chart and a pie chart of emotion distribution side by side
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Bar chart
    axs[0].bar(emotion_counts.index, emotion_counts.values)
    axs[0].set_title("Bar Chart - Emotion Distribution")
    axs[0].set_xlabel("Emotion")
    axs[0].set_ylabel("Count")

    # Pie chart
    axs[1].pie(emotion_counts, labels=emotion_counts.index, autopct='%1.1f%%', startangle=90)
    axs[1].set_title("Pie Chart - Emotion Distribution")

    # Save the chart to a BytesIO object
    chart_img = BytesIO()
    FigureCanvas(fig).print_png(chart_img)
    plt.close(fig)  # Close the figure explicitly to avoid the warning

    # Convert the BytesIO object to a base64-encoded string
    chart_img_base64 = base64.b64encode(chart_img.getvalue()).decode('utf-8')

    return chart_img_base64




if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
