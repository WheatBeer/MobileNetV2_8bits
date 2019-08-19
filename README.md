# MobileNetV2_8bits
MobileNetV2 8-bits Precision Validation & Retraining

<br />

## Dependencies
- [Pytorch][pytorch] (ver.1.1.0)
- torchvision
- tqdm (for progress bar)
- You can check other dependencies on top of *.py files

<br />

## MobileNetV2(Model + Pretrained weights & biases)
- Paper: ["Inverted Residuals and Linear Bottlenecks"][paper]
- Model Architecture: [model_summary.txt][model_summuary.txt] or 
```python3 model_summary.py```
- [Model Code][code] & [Imagenet Dataset][imagenet]

  ### Top 1 & Top 5
  - Using pretrained model(./data/mobilenet_v2-b0353104.pth)
  - Top 1 Accuracy: 71.88 % 	 
  - Top 5 Accuracy: 90.29 %

<br />

## Usage

  ### inference.py
  - Inference form an image.
  - Run on CPU and GPU.
  ~~~
  $ python3 inference.py -h
  usage: inference.py [-h] [-w PATH] [-i PATH]
  
  Inference only one image

  optional arguments:
    -h, --help                    show this help message and exit
    -w PATH, --weights PATH       Pretrained parameters PATH | Default: ./data/mobilenet_v2-b0353104.pth                      
    -i PATH, --input PATH         Input image PATH | Default: ./data/dog.jpg                
  ~~~
  
  <br />
  
  ### validation.py
  - Validate a trained model with ImageNet validation set.
  - Run on CPU and GPU.
  ~~~
  $ python3 validation.py -h
  usage: validation.py [-h] [-b #] [-p PATH] [-w PATH]
  
  Float Shift Validation

  optional arguments:
    -h, --help                   show this help message and exit
    -b #, --batch #              Batch Size | Default: 400
    -p PATH, --path PATH         Imagenet Dataset PATH | Default: /Data/ImageNet/ILSVRC2012/                
    -w PATH, --weights PATH      Pretrained parameters PATH | Default: ./data/mobilenet_v2-b0353104.pth
  ~~~
  - Results
  <b>(will be added soon)</b>
  
  <br />
  
  ### train.py
  - 
  - Run on only GPU.
  ~~~
  $ python3 train.py -h
  usage: train.py [-h] [-b #] [-e #] [-l #] [-d T/F] [--pretrained T/F] [-s T/F] [-p PATH] [-w PATH]

  Training MobileNetV2

  optional arguments:
    -h, --help                  show this help message and exit
    -b #, --batch #             Batch Size | Default: 400
    -e #, --epoch #             Epoches | Default: 1
    -l #, --lr #                Learning Rate | Default: 0.045
    -d T/F, --decay T/F         Learning Rate Decay | Default: True
    --pretrained T/F            Train from pretrained model | Default: True
    -s T/F, --save T/F          Save all models after every epoch(True) | Save best model(False)
    -p PATH, --path PATH        Imagenet Dataset PATH | Default: /Data/ImageNet/ILSVRC2012/
    -w PATH, --weights PATH     Pretrained parameters PATH | Default: ./data/mobilenet_v2-b0353104.pth
  ~~~
  - Results
  <b>(will be added soon)</b>
  ~~~
  python3 train.py -e 10 -l 0.001 -d 0
  ~~~

[pytorch]: https://pytorch.org/
[paper]: https://arxiv.org/abs/1801.04381
[code]: https://pytorch.org/hub/pytorch_vision_mobilenet_v2/
[model_summuary.txt]: https://github.com/WheatBeer/MobileNetV2_8bits/blob/master/model_summary.txt
[imagenet]: http://www.image-net.org/challenges/LSVRC/2012/nonpub-downloads
