from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    transcript = get_transcript(video_id)
    if transcript is None:
        return "Transcript not found", 404
    summary = get_summary(transcript)
    if summary is None:
        return "Summary generation failed", 500
    return summary, 200

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def get_summary(transcript):
    try:
        summariser = pipeline('summarization')
        if summariser is None:
            print("Summariser pipeline initialization failed")
            return None
        summary = ''
        for i in range(0, (len(transcript)//1000)+1):
            summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
            summary = summary + summary_text + ' '
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None

if __name__ == '__main__':
    app.run()
