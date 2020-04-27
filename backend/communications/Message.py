from hcwtracker import settings


def construct_message(message_type, user, extra):
    language = user.facility.language.language_name
    message_main = settings.MESSAGES[language][message_type]
    message_template = message_main["message"].replace('{first_name}', user.first_name)
    for key in extra:
        message_template.replace('{'+key+'}', extra[key])

    message = {
        "header": message_main["header"],
        "message": message_template
    }
    return message
