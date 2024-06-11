from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np 
import joblib

# Đọc dữ liệu từ file csv 
data = pd.read_csv('data_conver.csv', encoding='utf-8')

# Lấy dữ liệu cho x từ cột 'Pattern'
x = np.array(data['Pattern'])

# Lấy nhãn cho biến đầu ra y từ cột 'Tag'
y= np.array(data['Tag'])

# véc tơ hóa dữ liệu thành vector tf-idf
vectorizer = TfidfVectorizer()
x = vectorizer.fit_transform(x)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=16)

# khởi tạo và huấn luyện mô hình svm 
svm_model = SVC(kernel='linear')
svm_model.fit(x_train,y_train)

# đánh giá mô hình với dữ liệu test
y_predict = svm_model.predict(x_test)

# Lưu mô hình training 
joblib.dump(svm_model, 'model_conversation.joblib')

joblib.dump(vectorizer, 'vectorizer_conver.joblib')

# đánh giá kết quả mô hình 
print(classification_report(y_test, y_predict))