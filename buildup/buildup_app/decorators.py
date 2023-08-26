
# Decorator for __str__ functions,
# returning a 'not available' sentence,
# when the object's 'is_deleted' field is True.
def deleted_selector(func):
    def wrapper(*args, **kwargs):
        sentence = "The object you have been looking for is not available anymore."
        result = func(*args, **kwargs, sentence=sentence)
        return result
    return wrapper
