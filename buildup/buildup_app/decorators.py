
# Decorator for __str__ functions returning a 'not available' sentence
# when the object 'is_deleted' field is True:
def deleted_selector(func):
    def wrapper(*args, **kwargs):
        sentence = "The object you have been looking for is not available anymore."
        result = func(*args, **kwargs, sentence=sentence)
        return result
    return wrapper


# # Test -
# @deleted_selector
# def my_function(sentence):
#     print(sentence)
#
# my_function()
