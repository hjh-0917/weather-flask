from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "b8cc9f8b378f3baf0ad972080ccc3a79"

korean_to_english = {
    "서울": "Seoul",
    "부산": "Busan",
    "대구": "Daegu",
    "인천": "Incheon",
    "광주": "Gwangju",
    "대전": "Daejeon",
    "울산": "Ulsan",
    "세종": "Sejong",
    "경기": "Gyeonggi-do",
    "강원": "Gangwon-do",
    "충북": "Chungcheongbuk-do",
    "충남": "Chungcheongnam-do",
    "전북": "Jeollabuk-do",
    "전남": "Jeollanam-do",
    "경북": "Gyeongsangbuk-do",
    "경남": "Gyeongsangnam-do",
    "제주": "Jeju"
}

def get_weather(korean_city):
    city_en = korean_to_english.get(korean_city)
    if not city_en:
        return None, f"지원하지 않는 도시명입니다: {korean_city}"
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_en}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return (temp, desc), None
    else:
        return None, "날씨 정보를 불러오는데 실패했습니다. API 키와 도시명을 확인하세요."

@app.route("/", methods=["GET", "POST"])
def index():
    weather_info = None
    error = None
    
    if request.method == "POST":
        city_input = request.form.get("city")
        weather_info, error = get_weather(city_input)
    
    return render_template("index.html", weather=weather_info, error=error)

if __name__ == "__main__":
    app.run(debug=True)
