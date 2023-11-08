from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold


import pandas as pd
import numpy as np
import torch

from typing import Tuple
import os


from torch.utils.data import Dataset, DataLoader

torch.multiprocessing.set_sharing_strategy('file_system')

def prepare_train(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    """
    Preprocesses the input dataframe for training.

    Args:
        df (pandas.DataFrame): The input dataframe.

    Returns:
        tuple: A tuple containing:
            - numpy.ndarray: The preprocessed feature matrix.
            - pandas.Series: The target variable.
            - sklearn.preprocessing.StandardScaler: The fitted scaler object.

    Example:
        >>> df=pd.read_csv("train.csv", index_col='id')
        >>> X_train, y_train, scaler = prepare_train(df)
    """
    categorical_cols = ["hearing(left)", "hearing(right)","dental caries"]
    numerical_cols = [col for col in df.columns if col not in categorical_cols]

    df["bmi"] = df["weight(kg)"] / (df["height(cm)"]/100)**2
    df.drop(["height(cm)", "weight(kg)"], axis=1, inplace=True)

    y = df["smoking"]

    numerical_cols.remove("height(cm)")
    numerical_cols.remove("weight(kg)")
    numerical_cols.remove("smoking")
    numerical_cols.append("bmi")
    df.drop(["smoking"],axis=1,inplace=True)

    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    return df.to_numpy(), y.to_numpy(), scaler


def prepare_test(df: pd.DataFrame, scaler: StandardScaler) -> np.ndarray:
    """
    Preprocesses the input dataframe for testing.

    Args:
        df (pandas.DataFrame): The input dataframe.
        scaler (sklearn.preprocessing.StandardScaler): The fitted scaler object from prepare_train.

    Returns:
        numpy.ndarray: The preprocessed feature matrix.

    Example:
        >>> df=pd.read_csv("test.csv", index_col='id')
        >>> X_test = prepare_test(df, scaler)
    """
    categorical_cols = ["hearing(left)", "hearing(right)", "dental caries"]
    numerical_cols = [col for col in df.columns if col not in categorical_cols]
    df["bmi"] = df["weight(kg)"] / (df["height(cm)"]/100)**2
    df.drop(["height(cm)", "weight(kg)"], axis=1, inplace=True)
    numerical_cols.remove("height(cm)")
    numerical_cols.remove("weight(kg)")
    numerical_cols.append("bmi")
    df[numerical_cols] = scaler.transform(df[numerical_cols])
    return df.to_numpy()



class CustomDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        x_sample = self.X[idx]
        y_sample = self.y[idx]
        return x_sample.astype("float64"), y_sample.astype("float64")
    

    

def get_data_loaders(X: np.ndarray, y: np.ndarray, batch_size = 32) -> Tuple[DataLoader, DataLoader]:
    """
    Returns train and validation data loaders for the given input data and labels.

    Args:
        X (numpy.ndarray): Input data.
        y (numpy.ndarray): Labels.

    Returns:
        tuple: A tuple containing the train and validation data loaders.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, shuffle=True, stratify=y)
    train_dataset = CustomDataset(X_train, y_train)
    val_dataset = CustomDataset(X_test, y_test)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, num_workers=4, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, num_workers=4, pin_memory=True)
    return train_loader, val_loader



def get_cv_data_loaders(X, y, n_splits=5, batch_size=32):
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    for train_index, val_index in skf.split(X, y):
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        train_dataset = CustomDataset(X_train, y_train)
        val_dataset = CustomDataset(X_val, y_val)

        train_loader = DataLoader(train_dataset, batch_size=32, num_workers=4, pin_memory=True)
        val_loader = DataLoader(val_dataset, batch_size=32, num_workers=4, pin_memory=True)

        yield train_loader, val_loader


def get_train_dataloaders(X: np.ndarray, y: np.ndarray, batch_size = 32) -> Tuple[DataLoader, DataLoader]:

    train_dataset = CustomDataset(X, y)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, num_workers=4, pin_memory=True)
    return train_loader
