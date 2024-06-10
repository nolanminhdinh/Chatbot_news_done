import joblib
import json 
# load model training
loaded_model_svm = joblib.load('model_intent_detection.joblib')

#Load model vector h
vectorizer = joblib.load('vectorizer.joblib')


data_input= " What precious stone is a form of pure carbon"

data_processing =vectorizer.transform([data_input]).toarray()
predict = loaded_model_svm.predict(data_processing)

x= predict[0]

with open( 'label_question_detect.json', 'r',encoding='utf-8') as file:
    data = json.load(file)

# hàm in ra các phần tử liên quan đến phần predict được trả về 
def get_definition_and_trans(word): 
    result = {}
    for category, values  in data.items():
        for subcategory, translation in values['types'].items():
            if subcategory  == word:
                result['translation'] = translation
                result['definition'] =  values['definition']
                return result 
    return None

result = get_definition_and_trans(x)

print(f"Chủ đề {x}: {result['translation']}")
print( f'Thuộc Chủ đề lớn {result["definition"]}')
