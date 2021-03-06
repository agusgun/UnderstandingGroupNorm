import torch
import torch.nn as nn

from models import build_network
from dataset import build_data_loader
from utils.normalization_layer import GroupNorm2d, GNPLusSequentialBNFirst, GNPlusSequentialGNFirst, GNPlusParallel

def assert_norm_layer(model_name, model, correct_class_layer):
    if model_name == 'VGG16':
        assert isinstance(model.features[1], correct_class_layer)
        assert isinstance(model.features[41], correct_class_layer)
    elif model_name == 'ResNet50':
        assert isinstance(model.norm1, correct_class_layer)
        assert isinstance(model.layer4[2].norm3, correct_class_layer)

# Identity
vgg16_model = build_network('VGG16', 10, normalization_layer_name=None)
assert_norm_layer('VGG16', vgg16_model, nn.Identity)
resnet50_model = build_network('ResNet50', 10, normalization_layer_name=None)
assert_norm_layer('ResNet50', resnet50_model, nn.Identity)

# BN
vgg16_model = build_network('VGG16', 10, normalization_layer_name='bn')
assert_norm_layer('VGG16', vgg16_model, nn.BatchNorm2d)
resnet50_model = build_network('ResNet50', 10, normalization_layer_name='bn')
assert_norm_layer('ResNet50', resnet50_model, nn.BatchNorm2d)

# GN
vgg16_model = build_network('VGG16', 10, normalization_layer_name='gn')
assert_norm_layer('VGG16', vgg16_model, GroupNorm2d)
resnet50_model = build_network('ResNet50', 10, normalization_layer_name='gn')
assert_norm_layer('ResNet50', resnet50_model, GroupNorm2d)

# GNPlusSequentialBNFirst
vgg16_model = build_network('VGG16', 10, normalization_layer_name='gn_plus_sequential_bn_first')
assert_norm_layer('VGG16', vgg16_model, GNPLusSequentialBNFirst)
resnet50_model = build_network('ResNet50', 10, normalization_layer_name='gn_plus_sequential_bn_first')
assert_norm_layer('ResNet50', resnet50_model, GNPLusSequentialBNFirst)

# GNPlusSequentialGNFirst
vgg16_model = build_network('VGG16', 10, normalization_layer_name='gn_plus_sequential_gn_first')
assert_norm_layer('VGG16', vgg16_model, GNPlusSequentialGNFirst)
resnet50_model = build_network('ResNet50', 10, normalization_layer_name='gn_plus_sequential_gn_first')
assert_norm_layer('ResNet50', resnet50_model, GNPlusSequentialGNFirst)

# GNPlusParallel
vgg16_model = build_network('VGG16', 10, normalization_layer_name='gn_plus_parallel')
assert_norm_layer('VGG16', vgg16_model, GNPlusParallel)
resnet50_model = build_network('ResNet50', 10, normalization_layer_name='gn_plus_parallel')
assert_norm_layer('ResNet50', resnet50_model, GNPlusParallel)

# Dataset #
train, _ = build_data_loader('cifar10', 8)
for im, label in train:
    assert len(im) == 8
    break

train, _ = build_data_loader('cifar100', 8)
for im, label in train:
    assert len(im) == 8
    break

train, _ = build_data_loader('svhn', 8)
for im, label in train:
    assert len(im) == 8
    break

# train, _ = build_data_loader('imagenet-mini', 8)
# for im, label in train:
#     assert len(im) == 8
#     break
