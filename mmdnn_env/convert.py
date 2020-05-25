#! /usr/bin/evn python
# -*- coding: utf-8 -*-

import torch
import torchvision.models as models
import argparse
import importlib.machinery as imm

MainModel = imm.SourceFileLoader("MainModel", "VGG_ILSVRC_19.py").load_module()

def create_vgg19_model(caffe_pt):
    vision_name2caffe_name = {
        "features.0" : "conv1_1",
        "features.2" : "conv1_2",
        "features.5" : "conv2_1",
        "features.7" : "conv2_2",
        "features.10": "conv3_1",
        "features.12": "conv3_2",
        "features.14": "conv3_3",
        "features.16": "conv3_4",
        "features.19": "conv4_1",
        "features.21": "conv4_2",
        "features.23": "conv4_3",
        "features.25": "conv4_4",
        "features.28": "conv5_1",
        "features.30": "conv5_2",
        "features.32": "conv5_3",
        "features.34": "conv5_4",
        "classifier.0": "fc6_1",
        "classifier.3": "fc7_1",
        "classifier.6": "fc8_1",
    }

    model = models.vgg19(pretrained=False)
    caffe_model = torch.load(caffe_pt)

    caffe_name2layer = {}
    for name, layer in caffe_model.named_modules():
        if name in vision_name2caffe_name.values():
            caffe_name2layer[name] = layer

    with torch.no_grad():
        for name, layer in model.named_modules():
            if name not in vision_name2caffe_name:
                continue
            caffe_name = vision_name2caffe_name[name]
            caffe_layer = caffe_name2layer[caffe_name]
            layer.state_dict()["weight"].copy_(caffe_layer.state_dict()["weight"])
            layer.state_dict()["bias"].copy_(caffe_layer.state_dict()["bias"])
            
    return model

def convert_model(src_pt, dst_pt):
    model = create_vgg19_model(src_pt)
    torch.save(model.state_dict(), dst_pt)

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src_pt", metavar="SRC_MODEL", type=str, help="src PyTorch model")
    parser.add_argument("dst_pt", metavar="DST_MODEL", type=str, help="dst PyTorch model")

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    convert_model(args.src_pt, args.dst_pt)

if __name__ == "__main__":
    main()
