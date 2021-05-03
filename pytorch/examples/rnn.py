import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch import optim
from dataset import SinCurve, to_tensor

class SimpleRNN(nn.Module):
    def __init__(self, hidden_size, out_size):
        super().__init__()
        self.rnn = nn.RNN(out_size, hidden_size, nonlinearity="tanh")
        self.fc = nn.Linear(hidden_size, out_size)
        self.reset_state()

    def reset_state(self):
        self.hidden = None

    def unchain(self):
        if self.hidden is not None:
            # https://discuss.pytorch.org/t/solved-training-a-simple-rnn/9055
            self.hidden.detach_()

    def __call__(self, x):
        h, self.hidden = self.rnn(x, self.hidden)
        y = self.fc(h)
        return y

if False:
    from torchviz import make_dot

    rnn = nn.RNN(1, 10, nonlinearity="tanh")
    x0 = to_tensor(np.random.randn(1, 1)[np.newaxis, :])
    y, _ = rnn(x0)
    dot = make_dot(y, params=dict(rnn.named_parameters()))
    # https://graphviz.readthedocs.io/en/stable/api.html#graphviz.Graph.render
    dot.render("rnn", cleanup=True, format="png")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if True:
    max_epoch = 100
    batch_size = 30
    hidden_size = 100
    bptt_length = 30

    train_set = SinCurve(train=True)
    dataloader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=False)
    seqlen = len(dataloader)

    model = SimpleRNN(hidden_size, 1)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters())

    for epoch in range(max_epoch):
        model.reset_state()
        loss, count = torch.tensor(0.), 0

        for x, t in dataloader:
            y = model(x)
            loss += criterion(y, t)
            count += 1

            if count % bptt_length == 0 or count == seqlen:
                model.zero_grad()
                loss.backward()
                model.unchain()
                loss.detach_()
                optimizer.step()

        avg_loss = loss.item() / count
        print('| epoch %d | loss %f' % (epoch + 1, avg_loss))

    xs = np.cos(np.linspace(0, 4 * np.pi, 1000))
    model.reset_state()
    model.eval()
    pred_list = []

    with torch.no_grad():
        for x in xs:
            x = to_tensor(np.array(x).reshape(1, 1)[np.newaxis, :])
            y = model(x)
            pred_list.append(float(y.data))

    plt.plot(np.arange(len(xs)), xs, label='y=cos(x)')
    plt.plot(np.arange(len(xs)), pred_list, label='predict')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.savefig("result.png")
