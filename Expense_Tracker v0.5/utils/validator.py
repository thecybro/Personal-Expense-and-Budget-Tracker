"""Only allows float value to be entered."""
def validate_float(value: str):
    '''To allow only floats.'''
    if value == "":
        return True
    try:
        float(value)
        return True
    except ValueError:
        return False

"""Only allows integer value to be entered."""
def validate_int(value):
    if value == "" or value.isdigit():
        return True
    else:
        return False
