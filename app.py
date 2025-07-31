from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# ✅ OpenWeatherMap API 키 가져오기 (Render 환경변수 OR 로컬 변수)
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "여기에_테스트용_API키")

# ✅ 한글 도시명 → 영어 도시명 변환
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

@app.route("/", methods=["GET", "POST"])
def index():
    weather_info = None

    if request.method == "POST":
        city_kor = request.form.get("city")
        city_eng = korean_to_english.get(city_kor)

        if not city_eng:
            weather_info = f"지원하지 않는 도시명입니다: {city_kor}"
        else:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_eng}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                weather_info = f"{city_kor}({city_eng})의 현재 온도는 {temp}°C, 날씨는 '{desc}' 입니다."
            else:
                weather_info = "날씨 정보를 불러오는데 실패했습니다. API 키와 도시명을 확인하세요."

    return render_template("index.html", weather=weather_info)

# ✅ Render 배포용 (0.0.0.0 + 동적 PORT)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
