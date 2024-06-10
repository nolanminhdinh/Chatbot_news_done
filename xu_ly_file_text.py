import re 
import csv

# mở file để đọc và file csv để ghi
with open('train_5500label.text') as file, open('train5500.csv','w', newline= '') as csvfile:
    # tạo đối tượng writer csv 
    writer = csv.writer(csvfile)
    # viết header cho file csv 
    writer.writerow(['Classes', 'Definition','Questions'])

    # đọc từng dòng và xử lý file 
    for line in file: 
        # tách chữ ra 3 cột 
        match = re.match(r'^([A-Z]+):(\w+)\s(.+)$', line)
        if match:
            classes =  match.group(1)
            definition =  match.group(2)
            questions = match.group(3)

            # viết  dòng vào file csv 
            writer.writerow([classes, definition, questions])