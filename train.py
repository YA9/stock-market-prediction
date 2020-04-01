import os
import pickle
import argparse

from train_loop import TrainLoop

def main(args):
    # Parse arguments
    fc = [int(f) for f in args.fc.split(",")]

    # LOAD DATA HERE
    inputs, labels, input_dim = None, None, None

    train_loop = TrainLoop(inputs=inputs,
                           labels=labels,
                           train_split=args.train_split,
                           val_split=args.val_split,
                           fc=fc,
                           input_dim=input_dim,
                           output_dim=1,
                           hidden_dim=args.hidden_dim,
                           n_layers=args.n_layers,
                           dropout=args.dropout,
                           lr=args.lr,
                           batch_size=args.batch_size,
                           l2_penalty=args.penalty,
                           log_period=args.log_period,
                           save_period=args.save_period,
                           output_dir=args.output_dir,
                           wandb=args.wandb,
                           wandb_name=args.wandb_name,
                           wandb_project=args.wandb_project)
    train_loop.train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Train LSTM Net")
    # Str arguments
    parser.add_argument('--output-dir',
                        type=str,
                        default='/tmp/output',
                        help="directory to save model to (default:/tmp/output)")
    parser.add_argument('--data',
                        type=str,
                        default='data/processed_dataset.pickle',
                        help="saved preprocessed data (default:\
                        data/processed_data.pickle)")

    # Hyperparameters
    parser.add_argument('--fc',
                        type=str,
                        default="128",
                        help='neurons per fully connected layer, formatted as \
                        \"a,b,c\". (default: 128)')
    parser.add_argument('--train-split',
                        type=float,
                        default=0.8,
                        help='proportion of the data to use for training \
                        (default: 0.8)')
    parser.add_argument('--val-split',
                        type=float,
                        default=0.1,
                        help='proportion of the data to use for val \
                        (default: 0.8)')
    parser.add_argument('--batch-size',
                        type=int,
                        default=512,
                        help='input batch size for training (default: 512)')
    parser.add_argument('--epochs',
                        type=int,
                        default=100,
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr',
                        type=float,
                        default=0.005,
                        help='learning rate (default: 0.01)')
    parser.add_argument('--penalty',
                        type=float,
                        default=0,
                        help="L2 regularization coefficient (default: 0)")
    parser.add_argument("--hidden-dim",
                        type=int,
                        default=512,
                        help="LSTM hidden dimensions (default: 512)")
    parser.add_argument("--n-layers",
                        type=int,
                        default=1,
                        help="LSTM layers (default: 1)")
    parser.add_argument('--log-period',
                        type=int,
                        default=50,
                        help='how many update steps to wait before logging\
                        (default: 100)')
    parser.add_argument('--save-period',
                        type=int,
                        default=500,
                        help='how many update steps to wait before saving\
                        (default: 500)')

    # WandB flags
    parser.add_argument('--wandb',
                        default=False,
                        action='store_true',
                        help="log the training with WandB. REQUIRES INSTALLING,\
                        CONFIGURING AND LOGGING INTO WANDB")
    parser.add_argument('--wandb-name',
                        type=str,
                        default=None,
                        help="WandB run name")
    parser.add_argument('--wandb-project',
                        type=str,
                        default="stock_predictions",
                        help="WandB project name (default: stock_predictions)")
    args = parser.parse_args()
    main(args)