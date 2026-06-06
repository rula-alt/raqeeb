from flask import Flask, render_template, request
from urllib.parse import urlparse
import re

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route("/scan", methods=["POST"])
def scan():
    url = request.form["url"]
    domain = urlparse(url).netloc
    suspicious_keywords = ["login", "verify", "bank", "secure", "account"]
    risk = 0
    reasons = []

    for word in suspicious_keywords:
        if word in domain.lower():
            risk += 15
            reasons.append(f"الدومين يحتوي على كلمة '{word}' مما قد يشير إلى محاولة احتيال")

    import re

    if url.startswith("http://"):
        risk += 50
        reasons.append("لا يستخدم بروتوكول HTTPS")

    if len(url) > 50:
        risk += 20
        reasons.append("الرابط طويل بشكل مريب")
    if "@" in url:
        risk += 30
        reasons.append("يحتوي على عنوان بريد إلكتروني")

    if "login" in url.lower():
        risk += 20
        reasons.append("يحتوي على كلمة 'login' مما قد يشير إلى صفحة تسجيل دخول مزيفة")

    if "verify" in url.lower():
        risk += 20
        reasons.append("يحتوي على كلمة 'verify' مما قد يشير إلى محاولة احتيال")

    if "bank" in url.lower():
        risk += 20
        reasons.append("يحتوي على كلمة 'bank' مما قد يشير إلى محاولة احتيال مصرفي")

    if "secure" in url.lower():
        risk += 15
        reasons.append("يحتوي على كلمة 'secure'")

    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        risk += 40
        reasons.append("يحتوي على عنوان IP بدلاً من اسم نطاق")

    if "-" in url:
        risk += 10
        reasons.append("يحتوي على شرطات كثيرة")

    if url.startswith("https://"):
        status = "آمن - يستخدم بروتوكول HTTPS"
    else:
        status = "غير آمن - لا يستخدم بروتوكول HTTPS"

    if risk >= 60:
        verdict = "موقع خطير 🔴"
        color = "red"
    elif risk >= 30:
        verdict = " موقع مشبوه 🟡"
        color = "yellow"
    else:
        verdict = " موقع آمن 🟢"
        color = "green"

    if risk >100:
        risk = 100

    if risk >= 60:
        recommendation = "لا تخل الموقع!! ولا تدخل أي بيانات حساسة."
    elif risk >= 30:
        recommendation = "تحقق من الرابط جيداً قبل إستخدامه!"
    else:
        recommendation = "يمكن تصفح الموقع مع اتباع ممارسات الأمان المعتادة."

    if risk >= 60:
        ai_analysis = "تم إكتشاف عدة مؤشرات خطر في الموقع!! ينصح بعدم إدخال أي بيانات حساسة."
    elif risk >= 30:
        ai_analysis = "الموقع يحتوي على بعض المؤشرات المشبوهة, يستحسن التحقق منه قبل الاستخدام"
    else:
        ai_analysis = "الموقع يبدو آمناً بناءً على التحليل الأولي, لكن دائماً تأكد من الحذر عند إدخال بياناتك."

    return render_template(
        "result.html",
        url=url,
        domain=domain,
        status=status,
        risk=risk,
        color=color,
        reasons=reasons,
        verdict=verdict,
        ai_analysis=ai_analysis,
        recommendation=recommendation
    )
if __name__ == "__main__":
    app.run(debug=True)