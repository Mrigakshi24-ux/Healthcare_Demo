import en_core_web_sm
from transformers import BertForQuestionAnswering, AutoTokenizer
from transformers import pipeline
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure_text_new import returnMedDict
from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import librosa
import soundfile as sf
import json
from Recognize_from_file import speech_recognize_continuous_from_file

nlp_ner = en_core_web_sm.load()
modelname = 'deepset/bert-base-cased-squad2'
model = BertForQuestionAnswering.from_pretrained(modelname)
tokenizer = AutoTokenizer.from_pretrained(modelname)
nlp_qa = pipeline('question-answering', model=model, tokenizer=tokenizer)

credential = AzureKeyCredential('6936534d3eaa4ee68ca1f4535f45218d')
endpoint='https://conversational-cognitive-service.cognitiveservices.azure.com/'
text_analytics_client = TextAnalyticsClient(endpoint, credential)

folder_path='audio_files'
testFile = 'sound.wav'

def returnText(speech_result):
    final_text = ''
    for i in range(len(speech_result)):
        final_text += (json.loads(speech_result[i].result.json)['DisplayText'])
    return final_text

def process_file(full_file_path):
    sr = speech_recognize_continuous_from_file(full_file_path)
    inp = returnText(sr)
    results= returnMedDict([inp], nlp_qa, text_analytics_client, value_dict)
    status['processing'] = 'Done'
    os.remove(full_file_path)
    data['display'] = results

app = Flask(__name__)
CORS(app)

@app.route('/getFile',methods=['POST'])
def getFile():
    try:
        global value_dict
        value_dict = {'Name':[],'Age':[],'Occupation':[],'Gender':[],
                'Medical condition':[], 'Symptoms/sign':[],
                'Time since the start of the condition':[], 
                'Body structure and direction affected':[], 
                'Course of condition':[],
                'Examination for condition':[], 
                'Medication':[{'Name':[], 'Frequency':[], 'Dosage':[], 'Time':[]}], 
                'Next visit':['In a week'],
                'Time of examination':[],
                'Medical History':[{'Asthma':[], 'Surgeries':[], 'Bleeding issues':[]}],
                'Dental History':[{'Previous tooth extraction or oral procedure':[]}],
                'Personal History':[{'Smoking':[], 'Drinking':[]}],
            }
        if(request.method=='POST'):
            file = request.files['file']
            arr, s = librosa.load(file, sr=16000)
            if file:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)   
                full_file_path = os.path.join(folder_path, testFile)
                sf.write(full_file_path, arr, 16000)
                print(full_file_path)

                sr = speech_recognize_continuous_from_file(full_file_path)
                inp = returnText(sr)
                results= returnMedDict([inp], nlp_qa, text_analytics_client, value_dict)
                os.remove(full_file_path)
            return jsonify(results)
    
    except Exception as e:
        print(e)
        return {'Status':'Error'}

if __name__ == '__main__':
    app.run(debug = True, host  = "0.0.0.0")


