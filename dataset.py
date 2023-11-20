import pandas as pd
import cv2
import numpy as np
from tqdm import tqdm
import os

def load_and_crop_images(file_paths):
    cropped_images = []
    for path in tqdm(file_paths):
        img = cv2.imread(os.path.join("./dataset/images/", path))
        img_crop = [img[:256, :, :], img[256:384, :128, :]]
        cropped_images.append(img_crop)
    return np.array(cropped_images)

def load_csv_data(csv_file):
    df = pd.read_csv(csv_file)
    file_paths = df['filename'].tolist()
    labels = df[['Throttle Value', 'Throttle State', 'Steering Value', 'Steering State']].values
    return file_paths, labels

def create_npz_file(X, y, output_file):
    np.savez(output_file, X=X, y=y)

def main(csv_file, output_file):
    file_paths, labels = load_csv_data(csv_file)

    batch_size = 1000  # Adjust this based on your available memory
    num_batches = len(file_paths) // batch_size

    X_batches = []
    y_batches = []

    for i in range(num_batches):
        print(f"Batch {i+1} / {num_batches}:")
        start_idx = i * batch_size
        end_idx = (i + 1) * batch_size

        batch_file_paths = file_paths[start_idx:end_idx]
        batch_labels = labels[start_idx:end_idx]

        batch_images = load_and_crop_images(batch_file_paths)

        X_batches.append(batch_images)
        y_batches.append(batch_labels)
        print()

    # Concatenate batches
    X = np.concatenate(X_batches, axis=0)
    y = np.concatenate(y_batches, axis=0)

    print(X.shape)
    print(X[0][0].shape)
    print(X[0][1].shape)
    print(y.shape)
    create_npz_file(X, y, output_file)

if __name__ == "__main__":
    csv_file_path = ["./dataset/labels/keys_1.csv", "./dataset/labels/keys_2.csv", "./dataset/labels/keys_3.csv", "./dataset/labels/keys_4.csv"]
    output_npz_file = ["./dataset/npz/data_10000", "./dataset/npz/data_20000", "./dataset/npz/data_30000", "./dataset/npz/data_40000", ]
    for i in range(len(csv_file_path)):
        print(f"\n\n Creating dataset {i+1} / {len(csv_file_path)}:")
        main(csv_file_path[i], output_npz_file[i])
