# Face_Liveness_Detection

## Data Collection
Use 'dataCollectiontest.py' file for collecting the dataset for two different classes 'real' & 'fake'

## Split the Data
Use 'SplitData.py' to split up the data into train,test,validation (7:2:1) for the model build up purpose.

## Training the model
You can use google colab's T4 GPU runtime env for training your model.
Refer 'Antispoofingmodel.ipynb' for google colab training.
For local trainng, make sure installed pytorch, cuda cores for gpu runtime on your local machine, then run the 'train.py' to train the model locally.

## Test the model

Run 'main.py' to test the model's performance on realtime.
