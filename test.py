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
        "content": "A great game",
        "categories": [
            "sportclass"
        ]
    },
    {
        "content": "the election was over",
        "categories": [
            "notsport",
            "politics"
        ]
    },
    {
        "content": "very clean match",
        "categories": [
            "sportclass"
        ]
    },
    {
        "content": "a clean but forgettable game",
        "categories": [
            "sportclass"
        ]
    },
    {
        "content": "it was a close election",
        "categories": [
            "politics",
            "notsport"
        ]
    },
    {
        "content": "a very close game",
        "categories": [
           
        ]
    }
]
'''

example_json_data2 =  '''[
    {
      "content": "our president somtimes like to play sports like football. He voted last election also",
      "categories": ["sportclass","politics"]
    }
    ]
    '''

doc='''
A very close game.

'''
example_json_data3 =  '''[
    {
        "content": "the election",
        "categories": [
            "notsport",
            "politics"
        ]
    },
        {
        "content": "close election",
        "categories": [
            "politics",
            "notsport"
        ]
    }
    ]
    '''
example_json_data4 =  '''[
    {
        "content": "the election was over",
        "categories": [
            "notsport",
            "politics"
        ]
    },
        {
        "content": "it was a close election",
        "categories": [
            "politics",
            "notsport"
        ]
    }
    ]
'''

model3=GroupByClassModel("model3")
model3.print_model_name()
model3.train(example_json_data)
model3.train(example_json_data2)
model3.get_categories(True)