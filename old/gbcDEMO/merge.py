from gbc import GBC as Classifier
from gbc import Merger
from iptc import IPTC_topics,IPTC_topictags #Import IPTC Topics And Tags

# Load in model1 that has already been trained
model1 = Classifier()
model1.load('standardizedclassvectors.json')

# This is the new document that is labeled as "Conflicts and War and Peace"
NewDocument =''' 
               The name "Rowley Roen" is used as part of this example to illustrate
               incremental learning using the merge functionality of the GBC module.
               The terms ( protest and terrorism ) in this document will ensure  
               this document gets implicitly tagged under the category of
               'Conflicts and War and Peace'.
             '''
# Create a new model using the new document/documents
model2 = Classifier()
model2.init(IPTC_topics,IPTC_topictags).MinKey(2)
model2.build(NewDocument) # only one new training document
model2.setweights()
model2.tojson('newclassvectors')


# Using the Merger from the GBC module, merge both models
models = []
models.append(model1)
models.append(model2)
merger = Merger()
model3 = merger.merge(models)
model3.tojson("mergedclassvectors")

# print(model1.predict("dead").getTopics())