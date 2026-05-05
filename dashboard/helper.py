def parse_ai_blog(content):
    sections = {
        "title": "",
        "category": "",
        "summary": "",
        "body": ""
    }

    if not content:
        return sections

    try:
        sections["title"] = content.split("===BLOG_TITLE===")[1].split("===CATEGORY===")[0].strip()

        sections["category"] = content.split("===CATEGORY===")[1].split("===SHORT_SUMMARY===")[0].strip()

        sections["summary"] = content.split("===SHORT_SUMMARY===")[1].split("===BODY===")[0].strip()

        sections["body"] = content.split("===BODY===")[1].strip()

    except IndexError:
        pass  # AI returned unexpected format

    return sections
