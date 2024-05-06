import os
import random
import shutil
from itertools import islice

outputFolderPath = "Dataset/SplitData"
inputFolderPath = "Dataset/All"
classes = ["fake", "real"]
SplitRatio = {"train":0.6,"val":0.2,"test":0.2}

try:
    shutil.rmtree(outputFolderPath)
except OSError as e:
    os.mkdir(outputFolderPath)

# Directories to create

os.makedirs(f"{outputFolderPath}/train/images",exist_ok=True)
os.makedirs(f"{outputFolderPath}/train/labels",exist_ok=True)
os.makedirs(f"{outputFolderPath}/val/images",exist_ok=True)
os.makedirs(f"{outputFolderPath}/val/labels",exist_ok=True)
os.makedirs(f"{outputFolderPath}/test/images",exist_ok=True)
os.makedirs(f"{outputFolderPath}/test/labels",exist_ok=True)


#get the names
listNames = os.listdir(inputFolderPath)

uniqueNames = []
for name in listNames:
    uniqueNames.append(name.split('.')[0])
uniqueNames = list(set(uniqueNames))

# Shuffle
random.shuffle(uniqueNames)


# find the no of images in each folder
lenData = len(uniqueNames)
lenTrain = int(lenData*SplitRatio['train'])
lenVal = int(lenData*SplitRatio['val'])
lenTest= int(lenData*SplitRatio['test'])


# put the ramaining in the training
if lenData!=lenTrain+lenTest+lenVal:
    remaining = lenData-(lenTrain+lenTest+lenVal)
    lenTrain+=remaining

# Split the list
lengthToSplit = [lenTrain, lenVal, lenTest]
Input = iter(uniqueNames)
Output = [list(islice(Input,elem))for elem in lengthToSplit]
print(f"Total images:{lenData}\nSplit: {len(Output[0])} {len(Output[1])} {len(Output[2])}")


# COpy the files
sequence = ['train', 'val' , 'test']
for i,out in enumerate(Output):
    for filename in out:
        shutil.copy(f'{inputFolderPath}/{filename}.txt',f'{outputFolderPath}/{sequence[i]}/labels/{filename}.txt')
        shutil.copy(f'{inputFolderPath}/{filename}.jpg',f'{outputFolderPath}/{sequence[i]}/images/{filename}.jpg')


print("Splie process completed...")

# Creating data.yaml file
dataYaml = f'path: ../Data\n\
train: ../train/images\n\
val: ../val/images\n\
test: ../test/images\n\
\n\
nc: {len(classes)}\n\
names: {classes}'



f = open(f"{outputFolderPath}/data.yaml",'a')
f.write(dataYaml)
f.close()


print("Data.yaml file creates...")

