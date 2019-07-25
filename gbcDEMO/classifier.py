from gbc import GBC as Classifier
# Load in model that has already been trained
model1 = Classifier()
model1.load('standardizedclassvectors.json')
# The new document to be labeled
NewDocument1 =''' 
               More than 200 workers on breadline as 
               company closes down two of its operations
             '''
# Get all related categories and coressponding weights
MultiLabelResult = model1.predict(NewDocument1).getTopics()
# Get Category with higest weight
HighestResult  = model1.predict(NewDocument1).getTopic()
print(HighestResult)
print(MultiLabelResult)


# print(HighestResult)
# ('Labor', 2.8066731200801307)

# print(MultiLabelResult)

# {
# 	'Art and Culture': 1.2110519039414278,
# 	'Conflicts and War and Peace': 0.617441445019157,
# 	'Crime': 0.9395824945767677,
# 	'Disaster and Accidents': 0.6674548225074557,
# 	'Economy': 1.5285844948537626,
# 	'Education': 0.7129532113587717,
# 	'Environment': 0.9974623497221178,
# 	'Health': 0.49627275051802117,
# 	'Human Interest': 0.5316089626203007,
# 	'Labor': 2.8066731200801307,
# 	'Lifestyle and Leisure': 0.6207076720866188,
# 	'Politics': 0.6207252239374514,
# 	'Religion and Belief': 0.4166155287198772,
# 	'Science and Technology': 0.6567013434317349,
# 	'Society': 0.4614997965237786,
# 	'Sport': 0.7146648801026267
# }

