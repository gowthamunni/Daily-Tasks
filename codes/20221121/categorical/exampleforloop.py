import tensorflow as tf
import numpy as np


model = tf.keras.applications.VGG16()
layers = model.layers



layers_convolution = []
layers_dense = []
for layer in layers:
    if 'filters'in layer.get_config():
        layers_convolution.append(layer)
    if 'units' in layer.get_config():
        layers_dense.append(layer)


conv_fil_range = {}
conv_bias_range = {}
for layer in layers_convolution:
    filters = layer.filters
    layer_name = layer.name
    filter_weight = layer.get_weights()[0].transpose([3,0,1,2])
    bias = layer.get_weights()[1]


    inter_fil_list = []
    for filter_num in range(filters):
        inter_weights = filter_weight[filter_num, : , :, : ]
        f_min, f_max = np.min(inter_weights), np.max(inter_weights)
        inter_fil_list.append((f_min, f_max))

    b_min, b_max = np.min(bias), np.max(bias)
    
    conv_fil_range[layer_name] = inter_fil_list
    conv_bias_range[layer_name] = (b_min, b_max)




dense_weight_range = {}
dense_bias_range = {}
for layer in layers_dense:
    units = layer.units
    layer_name = layer.name
    dense_weights = layer.get_weights()[0].transpose()
    dense_bias = layer.get_weights()[1]

    inter_dweight_list = []
    for unit_idx in range(units):
        inter_weights = dense_weights[unit_idx, : ]
        d_min, d_max = np.min(inter_weights), np.max(inter_weights)
        inter_dweight_list.append((d_min, d_max))
    
    b_min, b_max = np.min(dense_bias), np.max(dense_bias)

    dense_weight_range[layer_name] = inter_dweight_list
    dense_bias_range[layer_name] = (b_min, b_max)

