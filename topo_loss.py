# Example from README
from topologylayer.nn import AlphaLayer, BarcodePolyFeature
import torch, numpy as np, matplotlib.pyplot as plt

def gen_circle(radius=1, num_samples=50):
    theta = np.linspace(0, 2 * np.pi, num_samples)
    x, y = radius * np.cos(theta), radius * np.sin(theta)
    return np.stack((x, y), axis=-1)

def gen_random_cloud(interval=(-1, 1), num_samples=10):
    points = (interval[1] - interval[0]) * np.random.random_sample((num_samples, 2)) + interval[0]
    return points


if __name__ == "__main__":

    # random pointcloud
    np.random.seed(0)
    data = np.random.rand(100, 2)

    # optimization to increase size of holes
    layer = AlphaLayer(maxdim=1)
    x = torch.autograd.Variable(torch.tensor(data).type(torch.float), requires_grad=True)
    f1 = BarcodePolyFeature(1,2,0)
    optimizer = torch.optim.Adam([x], lr=1e-2)
    for i in range(100):
        optimizer.zero_grad()
        loss = -f1(layer(x))
        loss.backward()
        optimizer.step()

    # save figure
    y = x.detach().numpy()
    fig, ax = plt.subplots(ncols=2, figsize=(10,5))
    ax[0].scatter(data[:,0], data[:,1])
    ax[0].set_title("Before")
    ax[1].scatter(y[:,0], y[:,1])
    ax[1].set_title("After")
    for i in range(2):
        ax[i].set_yticklabels([])
        ax[i].set_xticklabels([])
        ax[i].tick_params(bottom=False, left=False)
    plt.savefig('holes.png')