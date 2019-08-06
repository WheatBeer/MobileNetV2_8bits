import os
import argparse
import torch
import torch.nn as nn
import torchvision
from torchvision import transforms
import torchvision.datasets as datasets
from utils.mobilenetv2 import MobileNetV2
from utils import accuracy, AverageMeter

def round_tensor(arr, n_digits):
    rounded = torch.round(arr * 2**n_digits) 
    rounded = rounded / (2**n_digits)
    return rounded

parser = argparse.ArgumentParser(description='Float Shift Validation')

parser.add_argument('-b', '--batch', type=int, metavar='SIZE', 
                    default=400, help='Batch Size | Default: 400')

parser.add_argument('-n', '--n-digits', type=int, default=0, 
                    metavar='N', help='Round N digits | Default: 0')

parser.add_argument('-p', '--path', metavar='PATH', 
                    default='/Data/ImageNet/ILSVRC2012/', 
                    help='Imagenet Dataset PATH | Default: /Data/ImageNet/ILSVRC2012/')

parser.add_argument('-w', '--weights', metavar='PATH', 
                    default='./data/mobilenet_v2-b0353104.pth',
                    help='Pretrained parameters PATH | Default: ./data/mobilenet_v2-b0353104.pth')



def main():
    args = parser.parse_args()
    
    # Data Load & Preprocessing
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    imagenet_path = args.path
    test_dir = os.path.join(imagenet_path, 'val')

    test_set = datasets.ImageFolder(test_dir, preprocess)
    test_loader = torch.utils.data.DataLoader(test_set,
                                              batch_size=args.batch,
                                              shuffle=True,
                                              num_workers=4)
    
    print('===> batch size:', args.batch, '| 1000 classes x 50 images') 
    
    # Initialize values
    losses = AverageMeter('Loss', ':.4e')
    top1 = AverageMeter('Top 1 accuracy', ':6.5f')
    top5 = AverageMeter('Top 5 accuracy', ':6.5f')
    
    # Define the model
    model = MobileNetV2()
    criterion = nn.CrossEntropyLoss()
    model.load_state_dict(torch.load(args.weights))
#     model = torch.load(pth_path)
    model.eval()
    
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print('===> Test on', device)
    model.to(device)
    if torch.cuda.device_count() > 1:
        model = nn.DataParallel(model)
        print('===> Using', torch.cuda.device_count(), 'GPUs!')
    
    # round up
    if args.n_digits > 0:
        print('===> Round up(', args.n_digits,')')
        for param in model.parameters():
            param.data = round_tensor(param.data, args.n_digits)

    # Foward
    print('===> Start inferencing!')
    with torch.no_grad():
        for i, data in enumerate(test_loader, 0):
            # get the inputs
            inputs, labels = data
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            prec1, prec5 = accuracy(outputs.data, labels.data, topk=(1, 5))
            losses.update(loss.data, inputs.size(0))
            top1.update(prec1, inputs.size(0))
            top5.update(prec5, inputs.size(0))
        print('===>', top1.__str__(),'\t', top5.__str__())
    print('===> Test is done!')
    return [top1.val, top1.avg , top5.val, top5.avg]


if __name__ == '__main__':
    main()