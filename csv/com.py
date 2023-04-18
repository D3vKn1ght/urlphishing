import csv

filename = "result7.csv" 


datakiet = {}
# Tạo danh sách các cột trong tập tin CSV
columns = ["url", "label", "type_detect", "datetime"]

# Mở tập tin CSV
cdetect = 0
with open(filename, mode='r') as file:
    # Đọc nội dung của tập tin CSV
    csv_reader = csv.DictReader(file, fieldnames=columns)
    count = 0
    # Lặp qua từng dòng trong tập tin CSV
    for row in csv_reader:
        # Truy cập vào các giá trị của từng cột theo tên cột
        url = row["url"].strip()
        label = row["label"]
        type_detect = row["type_detect"]
        datetime = row["datetime"]
        datakiet[url] = label
        if(label == "1"):
            cdetect += 1
        count +=1
    print(count)
    print("detect",cdetect)
    
    

# print(list(datakiet)[:1000])
filename = "test.csv" 
       
# Tạo danh sách các cột trong tập tin CSV
columns = ["","x"]

test = []
# Mở tập tin CSV
with open(filename, mode='r',encoding="UTF-8") as file:
    # Đọc nội dung của tập tin CSV
    csv_reader = csv.DictReader(file, fieldnames=columns)
    
    # Lặp qua từng dòng trong tập tin CSV
    for row in csv_reader:
        # Truy cập vào các giá trị của từng cột theo tên cột
        url = row["x"]
        test.append(url.strip())
        
output = []
count = 0
for  i in test:
    if(i.strip() in datakiet):
        output.append(datakiet[i])
        count += 1
    else:
        output.append("0")
        # print(i)
        
print("after map ", count)

with open("output.csv", "w",encoding="UTF-8") as f:
    f.write(f"stt, url, label\n")
    for i in range (len(output)):
        f.write(f"{i}, {test[i]}, {output[i]}\n")

