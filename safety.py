EMERGENCY_PATTERNS = [
    "severe chest pain",
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "can't breathe",
    "cannot breathe",
    "fainting",
    "unconscious",
    "heavy bleeding",
    "stroke",
    "severe allergic reaction",
    "ضيق شديد في التنفس",
    "صعوبة في التنفس",
    "ألم شديد في الصدر",
    "ألم في الصدر",
    "إغماء",
    "نزيف شديد",
    "جلطة",
    "حساسية شديدة",
]


def detect_emergency(text):
    normalized = text.lower().strip()

    matches = [
        pattern
        for pattern in EMERGENCY_PATTERNS
        if pattern in normalized
    ]

    return {
        "is_emergency": bool(matches),
        "matched_patterns": matches,
    }


def emergency_response(language="English"):
    if language == "Arabic":
        return (
            "⚠️ **قد تكون هذه حالة طارئة.**\n\n"
            "الأعراض التي وصفتها قد تستدعي تقييمًا طبيًا عاجلًا. "
            "لا تعتمد على HealTrip AI لتشخيص الحالة.\n\n"
            "**إذا كانت الأعراض شديدة أو تتفاقم، توجّه إلى أقرب قسم طوارئ "
            "أو اتصل بخدمات الطوارئ المحلية الآن.**\n\n"
            "إذا كنت قادرًا على ذلك بأمان، أخبرني أيضًا عن العمر، "
            "مدة الأعراض، وهل توجد صعوبة في التنفس أو إغماء."
        )

    return (
        "⚠️ **This may require urgent medical evaluation.**\n\n"
        "The symptoms you described can require prompt medical assessment. "
        "Do not rely on HealTrip AI to diagnose your condition.\n\n"
        "**If the symptoms are severe or worsening, go to the nearest "
        "emergency department or contact local emergency services now.**\n\n"
        "If you can do so safely, you can also tell me your age, "
        "how long the symptoms have been present, and whether you have "
        "difficulty breathing or fainting."
    )
