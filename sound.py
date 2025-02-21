import pyttsx3
import re

cons = ("b","c","d","đ","g","gh","h","k","l","m","n","ng",
        "ngh","nh","p","ph","q","r","s","t","th","tr","v","x")
vows = "aăâeêioôơuưyáắấéếíóốớúứýáắấéếíóốớúứýàầèềìòồờùừỳảẳẩẻểỉỏổởủửỷãẵẫẽễĩõỗỡũữỹạặậẹệịọộợụựỵ"
stress = ("c","ch","p","t")


dic = {
    "b":"bờ","c":"cờ","d":"dờ","đ":"đờ","g":"gờ","gh":"ghờ","h":"hờ","k":"ca","kh": "khờ","l":"lờ","m": "mờ","n":"nờ","ng": "ngờ","ngh":"nghờ","nh":"nhờ","p":"pờ","ph": "phờ",
    "qu":"quờ","r":"rờ","s":"sờ","t":"tờ","th":"thờ","tr":"trờ", "ch":"chờ", "v":"vờ" , "s":"sờ", "x" : "xờ"
}

def speak(text):
    engine = pyttsx3.init()
    vi_voice_id = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"
    engine.setProperty('voice', vi_voice_id)
    engine.say(text)
    engine.runAndWait()
    
def getTone(token1):
    tone =  ""
    if bool(re.search(r'[áắấéếíóốớúứý]',token1)):
        tone = "sắc"
    elif bool(re.search(r'[àầèềìòồờùừỳ]',token1)):
        tone = "huyền"
    elif bool(re.search(r'[ảẳẩẻểỉỏổởủửỷ]',token1)):
        tone = "hỏi"    
    elif bool(re.search(r'[ãẵẫẽễĩõỗỡũữỹ]',token1)):
        tone = "ngã" 
    elif bool(re.search(r'[ạặậẹệịọộợụựỵ]',token1)):
        tone = "nặng" 
    return tone
    
def removeTone(mid, post):
    new_s = mid[:]
    new_s = re.sub(r"[áàảạ]", "a",  new_s)
    new_s = re.sub(r"[ấầẩẫậ]", "â", new_s)
    new_s = re.sub(r"[ắằẳẵặ]", "ă", new_s)
    new_s = re.sub(r"[ếềểễệ]", "ê", new_s)
    new_s = re.sub(r"[éèẻẽẹ]", "e", new_s)
    new_s = re.sub(r"[íìỉĩị]", "i", new_s)
    new_s = re.sub(r"[óòỏõọ]", "o", new_s)
    new_s = re.sub(r"[ốồổỗộ]", "ô", new_s)
    new_s = re.sub(r"[ớờởỡợ]", "ơ", new_s)
    new_s = re.sub(r"[úùủũụ]", "u", new_s)
    new_s = re.sub(r"[ứừửữự]", "ư", new_s)
    new_s = re.sub(r"[ýỳỷỹỵ]", "y", new_s)
    
    if type(post) == list: postStr = "".join(post)
    if (postStr in stress): 
        new_s = addStress(new_s) 
        
    return "".join(new_s)

def addStress(mid):
    
    new_s = [item for item in mid]
    if (new_s[-1] == "a"):
       new_s[-1] = "á"
    if (new_s[-1] == "â"):
       new_s[-1] = "ấ"
    if (new_s[-1] == "ă"):
       new_s[-1] = "ắ"
    if (new_s[-1] == "ê"):
       new_s[-1] = "ế"
    if (new_s[-1] == "e"):
       new_s[-1] = "é"
    if (new_s[-1] == "i"):
       new_s[-1] = "í"
    if (new_s[-1] == "o"):
       new_s[-1] = "ó"
    if (new_s[-1] == "ô"):
       new_s[-1] = "ố"       
    if (new_s[-1] == "ô"):
       new_s[-1] = "ố" 
    if (new_s[-1] == "ơ"):
       new_s[-1] = "ớ"        
    if (new_s[-1] == "u"):
       new_s[-1] = "ú" 
    if (new_s[-1] == "ư"):
       new_s[-1] = "ú" 
    if (new_s[-1] == "y"):
       new_s[-1] = "ý"        

    return new_s

def sep(i, X, t):
  if ((i==len(s) or s[i] not in cons) and t == "head"):    
    token.append(X)
    t = "mid" 
    X = []
    sep(i,X,t)    
  elif ((i==len(s) or s[i] not in vows) and t == "mid"):    
    token.append(X)    
    token.append([] if i>len(s) else list(s[i:]))    
    
  else:
    sep(i+1,X+[s[i]],t)

def parse(s,i, X):    
    if (i>=len(s) or (i<len(s) and s[i] not in X)):
        return []
    else:
        return [s[i]] + parse(s,i+1,X)
        
def spell(s):
    
    head = parse(s,0, cons)
    mid = parse(s,len(head), vows)
    tail = parse(s,len(head)+len(mid), cons)

    token = [head,mid,tail]
    
    token1 = "".join(token[1])
    newMid = removeTone(token1,tail)
    
    tone = getTone(token1)
    strhead = "".join(token[0])
    if (strhead != "" and strhead in dic): strhead = dic[strhead]    
    strtail = "".join(token[2])
    
    if strtail != "" and strtail in dic: strtail = dic[strtail]
    
    result = (strhead + "-" + newMid + "".join(token[2]) + "-" + "".join(token[0]) + newMid + "".join(token[2])) if strhead != "" else ("".join(newMid) + "-" + "".join(token[2]) + "-" + "".join(newMid)) + "".join(token[2])
    printText = (strhead + " " + newMid + "".join(token[2]) + "-" + "".join(token[0]) + newMid + "".join(token[2])) if strhead != "" else ("".join(newMid) + "-" + "".join(token[2]) + "-" + "".join(newMid)) + "".join(token[2])
    
    if (strhead == "" and strtail == ""):
        result = "-".join(list(newMid)) + "".join(token[2]) + "-" + "".join(token[0]) + newMid
        printText = "-".join(list(newMid)) + "".join(token[2]) + "-" + "".join(token[0]) + newMid
    
    if (tone != ""): 
        printText = printText + " " + tone + " " + s
        result = result + ", " + tone + " " + s
        

    speak(result)
    return printText
    

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

s = ""
def clear_entry():
    #print(111)
    label2.config(text="")
    entry.delete(0, tk.END)
    
def on_submit():
    
    s = entry.get()  # Lấy giá trị từ ô nhập liệu
    printText = ""
    if s:
        
        for word in s.lower().split():
            printText = printText + "  " + spell(word)          
        
        label2.config(text=printText)        
        
    else:
        messagebox.showwarning("Cảnh báo", "Nhập từ cần đánh vần!")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Đánh vần Tiếng Việt:")
root.geometry("800x700")
root.option_add("*Font", ("Arial", 16))  # Font Arial, size 16
root.iconbitmap("spell.ico")

# Mở ảnh JPG hoặc PNG
image = Image.open("spell.jpg")  
image = image.resize((212, 300))  
photo = ImageTk.PhotoImage(image)
# Thêm ảnh vào Label
label_image = tk.Label(root, image=photo)
label_image.pack(side="left", anchor="n", padx=5)


# Tạo và đặt các widget vào cửa sổ
label = tk.Label(root, text="Nhập từ cần đánh vần:")
label.pack(pady=10)  # Đặt nhãn vào cửa sổ với khoảng cách padding dọc 10px
frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

# Tạo Entry
entry = tk.Entry(frame, font=("Arial", 26), fg="green")
entry.pack(side="left", ipadx=40)  # Để trống chỗ cho icon

# Tạo Button với dấu "X" để xóa nội dung
btn_clear = tk.Button(frame, text="✖", width=2, command=clear_entry)
btn_clear.pack(side="left", padx=5)


#entry = tk.Entry(root, font=("Arial", 26))
#entry.pack(pady=10, padx=(5, 10), fill="x")

label2 = tk.Label(root, text="", wraplength=570)
label2.pack(pady=10)  # Đặt nhãn vào cửa sổ với khoảng cách padding dọc 10px


button = tk.Button(root, text="Đánh vần", command=on_submit)
button.pack(pady=5)  # Đặt nút bấm vào cửa sổ

# Bắt đầu vòng lặp sự kiện
root.mainloop()

