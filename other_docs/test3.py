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
        "content": "The new healthcare bill passed in congress.",
        "categories": [
            "notsport",
            "politics"
        ]
    },
    {
        "content": "The soccer team won the championship.",
        "categories": [
            "sportclass"
        ]
    },
    {
        "content": "The stock market experienced a major crash.",
        "categories": [
            "notsport",
            "finance"
        ]
    },
    {
        "content": "The basketball playoffs are heating up. match",
        "categories": [
            "sportclass"
        ]
    },
    {
        "content": "The latest scientific discovery could revolutionize medicine.",
        "categories": [
            "notsport",
            "science"
        ]
    }
]
'''

model3=GroupByClassModel("model3")
model3.print_model_name()
model3.train(example_json_data)
# model3.train(example_json_data2)
model3.get_categories(True)
# model3.classify("The football match ended with a spectacular goal")
# model3.classify("The presidential debate was intense.")


def classify_phrase(phrase, model:GroupByClassModel):
    '''classify_phrase'''
    prediction = model.classify(phrase)
    print(f"The predicted category for the phrase '{phrase}' is: {prediction}")

# Sample phrases
phrases = [
    "The football match ended with a spectacular goal.",
    "The presidential debate was intense.",
    "A thrilling basketball game took place last night.",
    "The new healthcare policy has been implemented.",
    "The cricket match was rained out.",
    "The mayor delivered a powerful speech at the conference.",
    "The hockey game went into overtime.",
    "The economic summit concluded with promising agreements.",
    "The baseball team won their championship game.",
    "The environmental activist spoke passionately at the rally."
]

# Test the classifier on each sample phrase
for p in phrases:
    classify_phrase(p, model3)