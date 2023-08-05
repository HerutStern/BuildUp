

def deleted_selector(func):
    def wrapper(*args, **kwargs):
        sentence = "What you have been looking for is not available anymore."
        result = func(*args, **kwargs, sentence=sentence)
        return result
    return wrapper


# # Work Test -
# @deleted_selector
# def my_function(sentence):
#     print(sentence)
#
# my_function()