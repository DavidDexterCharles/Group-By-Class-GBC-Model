# # pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring
# # pylint: disable=C0301:line-too-long
# # pylint: disable=W0707:raise-missing-from
# from pymongo import MongoClient
# from fastapi import APIRouter, Depends, HTTPException
# from app.api.pydanticmodels import Article
# from app.services.gbc import GroupByClassModel

# import cv2 as cv
# import numpy as np
# import matplotlib.pyplot as plt
# import tensorflow as tf
# from keras import datasets,layers,models
# from PIL import Image

# router = APIRouter()

# # Define your MongoDB connection URL
# # mongodb+srv://gbcuser:<password>@gbc.vny6qh7.mongodb.net/?retryWrites=true&w=majority&appName=gbc
# MONGO_URI = "mongodb+srv://gbcuser:gbcuser@gbc.vny6qh7.mongodb.net/?retryWrites=true&w=majority&appName=gbc"

# # Dependency function to create MongoDB client
# def get_mongo_client():
#     '''
#     get_mongo_client
#     '''
#     client = MongoClient(MONGO_URI)
#     yield client
#     client.close()

# @router.get("/cnnclasify")
# def cnnclasify():
#     class_names=['Plane','Car','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']
#     # img = cv.imread('images/horse-small.jpg')
#     img = cv.imread('images/deer.jpg')
#     img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
#     plt.imshow(img,cmap=plt.cm.binary)
#     model_file="image_classifier.keras"
#     model = models.load_model(model_file)
#     prediction = model.predict(np.array([img])/255)
#     index = np.argmax(prediction)
#     print(f'Prediction is {class_names[index]}')
#     plt.show()

# @router.get("/cnn")
# def cnn():
#     '''
#     Image classification with neural networks
#     https://youtu.be/t0EzVCvQjGE
#     '''

#     (training_images,training_labels),(testing_images,testing_labels)=datasets.cifar10.load_data()
#     training_images,testing_images=training_images/255,testing_images/255

#     # for i in range(16):
#     #     plt.subplot(4,4,i+1)
#     #     plt.xticks([])
#     #     plt.yticks([])
#     #     plt.imshow(training_images[i],cmap=plt.cm.binary)
#     #     plt.xlabel(class_names[training_labels[i][0]])
    
#     # plt.show()

#     training_images=training_images[:20000]
#     training_labels=training_labels[:20000]
#     testing_images=testing_images[:4000]
#     testing_labels=testing_labels[:4000]

#     model = models.Sequential()
#     model.add(layers.Conv2D(32,(3,3),activation='relu',input_shape=(32,32,3)))
#     model.add(layers.MaxPool2D((2,2)))
#     model.add(layers.Conv2D(64,(3,3),activation='relu'))
#     model.add(layers.MaxPool2D((2,2)))
#     model.add(layers.Conv2D(64,(3,3),activation='relu'))
#     model.add(layers.Flatten())
#     model.add(layers.Dense(64,activation='relu'))
#     model.add(layers.Dense(10,activation='softmax'))# so that there is one classification output that adds up to 1

#     model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

#     model.fit(training_images,training_labels,epochs=10,validation_data=(testing_images,testing_labels))

#     loss,accuracy= model.evaluate(testing_images,testing_labels)
#     print(f'Loss:{loss}')
#     print(f'Accuracy:{accuracy}')

#     model_file="image_classifier.keras"
#     model.save(model_file)

#     # model = models.load_model(model_file)

#     return "CNN VIEW"


# @router.get("/cnngbc")
# def cnngbc():
#     '''
#     Image classification with neural networks
#     https://youtu.be/t0EzVCvQjGE
#     '''

#     (training_images,training_labels),(testing_images,testing_labels)=datasets.cifar10.load_data()
#     training_images,testing_images=training_images/255,testing_images/255

#     # for i in range(16):
#     #     plt.subplot(4,4,i+1)
#     #     plt.xticks([])
#     #     plt.yticks([])
#     #     plt.imshow(training_images[i],cmap=plt.cm.binary)
#     #     plt.xlabel(class_names[training_labels[i][0]])
    
#     # plt.show()

#     training_images=training_images[:20000]
#     training_labels=training_labels[:20000]
#     testing_images=testing_images[:4000]
#     testing_labels=testing_labels[:4000]


#     image = Image.open("images/horse-small.jpg")  # Replace "example_image.jpg" with the path to your image file

#     # Convert the image to grayscale (if needed)
#     # image = image.convert("L")  # Uncomment this line if you want to convert the image to grayscale

#     # Convert the image to a NumPy array
#     image_array = np.array(image)

#     # Print the shape of the array (height, width, channels)
#     print("Image shape:", image_array.shape)

#     # Print the pixel values
#     print("Pixel values:")
#     print(image_array)


#     class_names=['Plane','Car','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']
#     model=GroupByClassModel(name="image_classifier_gbc",categories=class_names,increment_learning=False)
#     # model = models.Sequential()
#     # model.add(layers.Conv2D(32,(3,3),activation='relu',input_shape=(32,32,3)))
#     # model.add(layers.MaxPool2D((2,2)))
#     # model.add(layers.Conv2D(64,(3,3),activation='relu'))
#     # model.add(layers.MaxPool2D((2,2)))
#     # model.add(layers.Conv2D(64,(3,3),activation='relu'))
#     # model.add(layers.Flatten())
#     # model.add(layers.Dense(64,activation='relu'))
#     # model.add(layers.Dense(10,activation='softmax'))# so that there is one classification output that adds up to 1

#     # model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

#     # model.fit(training_images,training_labels,epochs=10,validation_data=(testing_images,testing_labels))

#     # loss,accuracy= model.evaluate(testing_images,testing_labels)
#     # print(f'Loss:{loss}')
#     # print(f'Accuracy:{accuracy}')

#     # model_file="image_classifier.keras"
#     # model.save(model_file)

#     return "CNN  GBC VIEW"