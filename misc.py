from torch import nn
from torch import optim
from torch.autograd import Variable
import torch
'''
def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1 or classname.find("Linear") !=-1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)
'''
def one_hot(labelTensor,batchSize,n_l,use_cuda=False,device=None):
    oneHot = - torch.ones(batchSize*n_l).view(batchSize,n_l)
    for i,j in enumerate(labelTensor):
        # Convert tensor to integer if needed
        j_int = j.item() if hasattr(j, 'item') else int(j)
        oneHot[i,j_int] = 1
    if use_cuda and device is not None:
        return Variable(oneHot).to(device)
    elif use_cuda:
        # Fallback for backward compatibility
        return Variable(oneHot).cuda()
    else:
        return Variable(oneHot)

def TV_LOSS(imgTensor,img_size=128):
    x = (imgTensor[:,:,1:,:]-imgTensor[:,:,:img_size-1,:])**2
    y = (imgTensor[:,:,:,1:]-imgTensor[:,:,:,:img_size-1])**2

    out = (x.mean(dim=2)+y.mean(dim=3)).mean()
    return out
