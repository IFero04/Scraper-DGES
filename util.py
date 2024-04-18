def extract_escolas(text):
    have_text = False
    result = ''
    for char in text:
        if char.isdigit() and have_text:
            break
        if char.isalpha():
            have_text = True
        result += char
    return result.strip()
            
def extract_cursos(text):
    have_text = False
    result = ''

    if text[0] == "L":
        result += 'L'
        text = text[1:]
    
    for i, char in enumerate(text):
        if char.isdigit() and have_text:
            if text[i -1] == "L":
                result = result[:-1]
            break
        if char.isalpha():
            have_text = True
        result += char
    return result.strip()
