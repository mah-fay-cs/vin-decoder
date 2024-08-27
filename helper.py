import re

def find_longest_match(patterns, text):
    patterns.sort(key=lambda x: len(list(x.keys())[0]), reverse=True)

    best_match = None
    max_matched_chars = 0

    for pattern_dict in patterns:
        for pattern, label in pattern_dict.items():
            match = re.match(pattern, text)
            if match:
                matched_chars = len(match.group(0))
                if matched_chars > max_matched_chars:
                    max_matched_chars = matched_chars
                    best_match = label
    return best_match

def refine_car_model_name(input_string):
    if input_string is None:
        return 'Unknown'
    words = input_string.split()
    result_words = []

    for word in words:
        if not any(char.isdigit() for char in word):
            if len(word) > 3:
                result_words.append(word.capitalize())
            else:
                result_words.append(word)
        else:
            result_words.append(word)

    return ' '.join(result_words)

def get_ar_model_name(df, en_model):
    filtered_df = df[(df['CAR_MODEL'].str.upper() == en_model.upper()) & df['CAR_MODEL_AR'].notna()]
    grouped_df = filtered_df.groupby('CAR_MODEL_AR').size().reset_index(name='count')
    max_row = grouped_df[grouped_df['count'] == grouped_df['count'].max()]
    if len(max_row['CAR_MODEL_AR'].values):
        return max_row['CAR_MODEL_AR'].values[0]
    return None

def get_ar_make_name(df, en_make):
    filtered_df = df[(df['CAR_MAKE'].str.upper() == en_make.upper()) & df['CAR_MAKE_AR'].notna()]
    grouped_df = filtered_df.groupby('CAR_MAKE_AR').size().reset_index(name='count')
    max_row = grouped_df[grouped_df['count'] == grouped_df['count'].max()]
    if len(max_row['CAR_MAKE_AR'].values):
        return max_row['CAR_MAKE_AR'].values[0]
    return None