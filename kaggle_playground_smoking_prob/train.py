from data_utils import get_data_loaders, prepare_train, get_cv_data_loaders, get_train_dataloaders
from engine import training_step, validation_step
from utils import print_trainable_parameters
from model import ClsModel1, ClsModel2, save_model, load_model

import pandas as pd
import torch
from torch import nn

df=pd.read_csv("data/train.csv", index_col='id')
X_train, y_train, scaler = prepare_train(df)


def k_fold_cross_validation_train():
    for fold, (train_dataloader, val_dataloader) in enumerate(get_cv_data_loaders(X_train, y_train, n_splits=5, batch_size=128)):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        torch.manual_seed(0)
        model  = ClsModel2(input_size=21, hidden_size=50,num_classes=1)
        optimzer = torch.optim.Adam(model.parameters(), lr=0.0001)
        loss_fn = nn.BCELoss()
        from torchmetrics import AUROC,Accuracy
        auroc = AUROC(num_classes=3,task='binary')
        accuracy = Accuracy(task='binary')
        train,val = get_data_loaders(X_train, y_train, batch_size=64)
        print(f"Fold: {fold}")

        for i in range(50):
            print(f"Epoch: {i}")
            average_loss, model, optimizer, scheduler = training_step(model, train_dataloader, loss_fn, optimzer, device)
            print(f"Average loss: {average_loss}")
            metrics = validation_step(model, val_dataloader, device, rocauc=auroc, accuracy=accuracy)
            print(f"Validation metrics: {metrics}")
            save_model(model=model, optimizer=optimizer, epoch=i,loss=average_loss,filename=f"model_{fold}")
        


def train():
    train_dataloader = get_train_dataloaders(X_train, y_train, batch_size=256)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    torch.manual_seed(0)
    model  = ClsModel2(input_size=21, hidden_size=50,num_classes=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
    loss_fn = nn.BCELoss()
    from torchmetrics import AUROC,Accuracy
    auroc = AUROC(num_classes=3,task='binary')
    accuracy = Accuracy(task='binary')
    train,val = get_data_loaders(X_train, y_train, batch_size=64)
    model, optimizer, epoch, loss, scheduler = load_model(model, optimizer, filename="saved_models/model_all_data.pt")
    optimizer.param_groups[0]['lr'] = optimizer.param_groups[0]['lr']/10
    for i in range(epoch,epoch+50):
            print(f"Epoch: {i}")
            average_loss, model, optimizer, scheduler = training_step(model, train_dataloader, loss_fn, optimizer, device)
            print(f"Average loss: {average_loss}")
            metrics = validation_step(model, train_dataloader, device, rocauc=auroc, accuracy=accuracy)
            print(f"Validation metrics: {metrics}")
            save_model(model=model, optimizer=optimizer, epoch=i,loss=average_loss,filename=f"model_all_data")

train()