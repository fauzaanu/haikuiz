import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def balance_markup(star_balance):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=f'You have {star_balance} ⭐', callback_data='balance')],
    ])


def alpha_space(string_to_convert):
    converted_string = str()
    for char in string_to_convert:
        if char.isalnum() or char == ' ':
            converted_string += char
    return converted_string


async def get_user_details(update):
    user_details = "ℹ️ User Details\n\n"

    if update.message:
        if update.message.chat.first_name:
            user_details += f'👤 First Name: {update.message.chat.first_name}\n'
        if update.message.chat.last_name:
            user_details += f'👤 Last Name: {update.message.chat.last_name}\n'
        if update.message.chat.username:
            user_details += f'📎 Username: @{update.message.chat.username}\n'
        if update.message.chat.id:
            user_details += f'🆔 Chat ID: {update.message.chat.id}\n'
    elif update.callback_query:
        if update.callback_query.message.chat.first_name:
            user_details += f'👤 First Name: {update.callback_query.message.chat.first_name}\n'
        if update.callback_query.message.chat.last_name:
            user_details += f'👤 Last Name: {update.callback_query.message.chat.last_name}\n'
        if update.callback_query.message.chat.username:
            user_details += f'📎 Username: @{update.callback_query.message.chat.username}\n'
        if update.callback_query.message.chat.id:
            user_details += f'🆔 Chat ID: {update.callback_query.message.chat.id}\n'

    return user_details


def remove_question_words(string_to_convert):
    question_words = ['who', 'what', 'when', 'where', 'why', 'how', 'which', 'whom']
    converted_string = str()
    for word in string_to_convert.split():
        if word.lower() not in question_words:
            converted_string += word + ' '
    return converted_string


def remove_verbs(string_to_convert):
    verbs = ['is', 'are', 'am', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
             'shall', 'will', 'should', 'would', 'may', 'might', 'must', 'can', 'could', "the"]
    prepositions = [
        'aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'amid', 'among', 'anti', 'around',
        'as', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'besides', 'between', 'beyond', 'but', 'by',
        'concerning', 'considering', 'despite', 'down', 'during', 'except', 'excepting', 'excluding', 'following',
        'for', 'from', 'in', 'inside', 'into', 'like', 'minus', 'near', 'of', 'off', 'on', 'onto', 'opposite',
        'outside',
        'over', 'past', 'per', 'plus', 'regarding', 'round', 'save', 'since', 'than', 'through', 'to', 'toward',
        'towards', 'under', 'underneath', 'unlike', 'until', 'up', 'upon', 'versus', 'via', 'with', 'within', 'without'
    ]
    verb_string = str()
    final_string = str()

    for word in string_to_convert.split():
        if word.lower() not in verbs:
            verb_string += word + ' '

    for word in verb_string.split():
        if word.lower() not in prepositions:
            final_string += word + ' '

    return final_string


async def alert_admin(message, context, update):
    user_details = await get_user_details(update)

    # alert admin
    await context.bot.send_message(
        chat_id=os.environ['ADMIN_CHAT_ID'],
        text=f'{user_details}\n\n{message}'
    )


async def get_journal_articles(question: str):
    "from the question grab some journal articles"
    import requests
    # https://www.doaj.org/api/search/articles/cognitive%20load?page=1&pageSize=20

    # publisher
    # year
    # author
    # link
    # abstract
    # title
    # created_date

    question = remove_question_words(alpha_space(remove_verbs(question)))
    base_url = "https://www.doaj.org/api/search/articles/"

    response = requests.get(f"{base_url}{question}?page=1&pageSize=2")
    response_json = response.json()

    if response_json['total'] == 0:
        return None
    else:
        response_str = str()
        response_str = process_response_str(response_json, response_str)
        return response_str


def escape_dot(string_to_convert):
    converted_string = str()
    for char in string_to_convert:
        if char == '.':
            converted_string += f'\{char}'
        elif char == '-':
            converted_string += f'\{char}'
        else:
            converted_string += char
    return converted_string


def process_response_str(response_json, response_str):
    articles = response_json['results']

    for article in articles:
        response_str += (f"📚 {alpha_space(article['bibjson']['title'])[0:100]} \. \. \."
                         f"\n[🔗 Link]({escape_dot(article['bibjson']['link'][0]['url'])})"
                         f"\n\n")
    return response_str


if __name__ == "__main__":
    pass
    # x = get_journal_articles("cognitive load")
    # print(x)
