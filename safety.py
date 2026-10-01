EMERGENCY_PATTERNS = [
    "severe chest pain",
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "cannot breathe",
    "can't breathe",
    "fainting",
    "unconscious",
    "heavy bleeding",
    "stroke",
    "severe allergic reaction",
    "ألم شديد في الصدر",
    "ألم في الصدر",
    "ضيق شديد في التنفس",
    "صعوبة في التنفس",
    "لا أستطيع التنفس",
    "إغماء",
    "فاقد الوعي",
    "نزيف شديد",
    "جلطة",
    "حساسية شديدة",
]


def detect_emergency(text):

    normalized = text.lower().strip()

    matches = []

    for pattern in EMERGENCY_PATTERNS:

        if pattern.lower() in normalized:
            matches.append(pattern)

    return {
        "is_emergency": len(matches) > 0,
        "matched_patterns": matches,
    }


def emergency_response(language="English"):

    if language == "Arabic":

        return """
### 🚨 قد تحتاج هذه الأعراض إلى تقييم طبي عاجل

الأعراض التي وصفتها قد تستدعي تقييماً طبياً سريعاً.

**HealTrip AI لا يشخّص الحالة ولا يمكنه استبعاد الحالات الخطيرة.**

إذا كانت الأعراض شديدة أو تتفاقم، توجّه إلى أقرب قسم طوارئ أو اتصل بخدمات الطوارئ المحلية.

لا تؤخر طلب الرعاية الطبية بسبب استخدام هذا التطبيق.
"""

    return """
### 🚨 Urgent medical evaluation may be appropriate

The symptoms you described may require prompt medical assessment.

**HealTrip AI does not diagnose conditions and cannot rule out serious causes.**

If symptoms are severe or worsening, go to the nearest emergency department or contact local emergency services.

Do not delay medical care because of this application.
"""
