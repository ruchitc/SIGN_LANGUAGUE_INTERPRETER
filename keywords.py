import string


def remove_punctuation(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


def find_keywords(text):
    if text is None:
        print("No input text provided.")
        return

    # Remove punctuation
    text = remove_punctuation(text)

    # Split the text into words
    words = text.split()

    # List of words to exclude
    words_to_exclude = ['am', 'is', 'are','was','were']

    # Remove specific words from the list
    filtered_words = [word for word in words if word.lower() not in words_to_exclude]

    # List of keywords to check against
    mp4_dataset = ['accessibility', 'accommondation', 'allthebest', 'amazing', 'availability', 'begin', 'bestofluck',
                   'bestwish', 'busy',
                   'cheerful', 'communicate', 'complete', 'congratulation', 'connection', 'cool', 'cost', 'deaf', 'do',
                   'does', 'engaged', 'enjoy', 'experience', 'family', 'fine', 'finsih', 'from', 'future', 'go', 'goal',
                   'good', 'goodafternoon', 'goodmorning', 'goodnight', 'happy', 'hearing', 'heart',
                   'home', 'house', 'how', 'i', 'important', 'incredible', 'internet', 'itsgreatconnectionwithyou',
                   'joyful', 'love', 'main', 'me', 'meet', 'money', 'my',
                   'name', 'nicetomeetyou', 'normalpreview', 'note', 'now', 'office', 'pen', 'please', 'previous',
                   'price', 'property', 'race', 'recored', 'run', 'sad', 'see', 'seeyoutommorow', 'skill',
                   'sorry', 'start', 'target', 'tea', 'thankyou', 'thatday', 'thedatbefore', 'thepreviosday', 'think',
                   'thismoment', 'thistime', 'time', 'today', 'tomorrow', 'value',
                   'vision', 'walk', 'watch', 'water', 'welcome', 'went', 'when', 'where', 'who', 'why', 'win', 'work',
                   'yesterday', 'you', 'your']

    # Filter keywords based on the remaining words
    keywords = [word.capitalize() for word in filtered_words if word in mp4_dataset]

    return keywords


