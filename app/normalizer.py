import dateparser

def normalize_data(date_phrase, time_phrase):
    parsed = dateparser.parse(
        f"{date_phrase} {time_phrase}",
        settings={"TIMEZONE": "Asia/Kolkata"}
    )

    return {
        "date": parsed.strftime("%Y-%m-%d"),
        "time": parsed.strftime("%H:%M")
    }
