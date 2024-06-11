from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np 
import joblib

# Đọc dữ liệu từ file CSV
data = pd.read_csv('train5500.csv', encoding='latin1')

# Lấy dữ liệu cho biến đầu vào x từ cột 'Questions'
x = np.array(data['Questions'])

# Lấy nhãn cho biến đầu ra y từ cột 'Definition'
y = np.array(data['Definition'])

# Chuyển đổi dữ liệu văn bản thành vectơ TF-IDF
vectorizer = TfidfVectorizer()
x = vectorizer.fit_transform(x)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42) #random_state để kết quả random cố định

# Khởi tạo và huấn luyện mô hình SVM
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# Đánh giá mô hình bằng dữ liệu test
y_pred = svm_model.predict(X_test)

# Lưu mô hình training
joblib.dump(svm_model, 'model_intent_detection.joblib')

# Lưu mô hình vector hóa
joblib.dump(vectorizer, 'vectorizer_detec.joblib')

# Đánh giá kết quả mô hình 
print(classification_report(y_test, y_pred))
