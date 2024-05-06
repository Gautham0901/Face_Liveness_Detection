from ultralytics import YOLO

model = YOLO('best.pt')

def main():
    model.train(data='Dataset/SplitData/dataOffline.yaml', epochs=1)
if __name__ == '__main__':
    main()