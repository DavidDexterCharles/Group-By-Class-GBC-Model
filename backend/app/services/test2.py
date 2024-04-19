#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace
#pylint: disable=C0301:line-too-long
#pylint: disable=C0103:invalid-name
from gbc import  GroupByClassModel
example_json_data =  '''[
    {
        "content": "Get rich quick with this amazing offer!",
        "categories": [
            "spam"
        ]
    },
    {
        "content": "Enlarge your bank account with our exclusive deal!",
        "categories": [
            "spam"
        ]
    },
    {
        "content": "Lose weight fast with our miracle pill!",
        "categories": [
            "spam"
        ]
    },
    {
        "content": "You've won a free vacation! Claim it now!",
        "categories": [
            "spam"
        ]
    },
    {
        "content": "A great game",
        "categories": [
            "sportclass"
        ]
    },
    {
        "content": "The election was over",
        "categories": [
            "notsport",
            "politics"
        ]
    },
    {
        "content": "Very clean match",
        "categories": [
            "sportclass"
        ]
    },
    {
        "content": "A clean but forgettable game",
        "categories": [
            "sportclass"
        ]
    },
    {
        "content": "It was a close election",
        "categories": [
            "politics",
            "notsport"
        ]
    },
    {
        "content": "A very close game",
        "categories": []
    }
]
'''



model3=GroupByClassModel("model3")
model3.print_model_name()
model3.train(example_json_data)
# model3.train(example_json_data2)
model3.get_categories(True)
model3.classify("Congratulations! You've been selected as the winner of our exclusive contest. Claim your prize now!")