import tensorflow as tf



def build_conv_block(inputs,param_dict):
    
    conv = tf.keras.layers.Conv2D(filters = filters, kernel_size = kernel_size, strides = strides, padding = pad)(inputs)
    sig = tf.keras.activations.sigmoid(conv)
    
    return tf.keras.layers.Multiply()([conv, sig])


def build_add_block(inputs, param_dict):

    conv_out1 = build_conv_block(inputs,  param_dict)
    conv_out2 = build_conv_block(conv_out1, param_dict)
    
    return tf.keras.layers.Add()([conv_out2, inputs])



inputs = tf.keras.Input(shape=shape)
conv_block = build_conv_block(inputs, param_dict)
conv_block_next = build_conv_block(conv_block, param_dict)

branchx_conv_block = build_conv_block(conv_block_next, param_dict)
add_block = build_add_block(branchx_conv_block, param_dict)
branchy_conv_block = build_conv_block(conv_block_next, param_dict)
concat = tf.keras.layers.concatenate([branchy_conv_block, add_block],axis = axis)

conv_block = build_conv_block(concat, param_dict)
conv_block_next = build_conv_block(conv_block, parm_dict)


branchx_conv_block = build_conv_block(conv_block_next, param_dict) 
add_block1 = build_conv_block(branchx_conv_block, param_dict)
add_block2 = build_conv_block(add_block1, param_dict)   
branchy_conv_block = build_conv_block(conv_block_next, param_dict)
concat = tf.keras.layers.concatenate([add_block2, branchy_conv_block], axis = axis)


conv_block = build_conv_block(concat, param_dict)
branchx_conv_block = build_conv_block(conv_block, param_dict)
branchx_right_conv_block = build_conv_block(branchx_conv_block, param_dict)
branchx_right_add_block1 = build_add_block(branchx_right_conv_block, param_dict)
branchx_right_add_block2 = build_add_block(branchx_right_add_block1, param_dict)
branchx_right_add_block3 = build_add_block(branchx_right_add_block2, param_dict)
branchx_left_conv_block = build_conv_block(branchx_conv_block, param_dict)
concat = tf.keras.layers.concatenate([branchx_left_conv_block, branchx_right_add_block])


branchx_conv_block = build_conv_block(concat, param_dict)
branchx_right_conv_block = build_conv_block(branchx_conv_block, param_dict)
branch_inside_right_conv = build_conv_block(branchx_right_conv_block, param_dict)
branch_inside_right_add = build_add_block(branch_inside_right_conv, param_dict)
branch_inside_left_conv = build_conv_block(branchx_right_conv_block, param_dict)
concat = tf.keras.layers.concatenate([branch_inside_right_add, branch_inside_left_conv],axis = axis)

branchx_right_conv_block = build_conv_block(concat, param_dict)
branchx_right_conv_block = build_conv_block(branchx_right_conv_block , param_dict)
maxpool1 = tf.keras.layers.MaxPool2D()(branchx_right_conv_block)
maxpool2 = tf.keras.layers.MaxPool2D()(maxpool1)
maxpool3 = tf.keras.layers.MaxPool2D()(maxpool2)
concat = tf.keras.layers.concatenate()([branchx_right_conv_block, maxpool1, maxpool2, maxpool3])

branchx_right_conv_block = build_conv_block(concat, param_dict)
branchx_right_conv_block = build_conv_block(branchx_right_conv_block, param_dict)
resize = tf.keras.layers.Resizing(height, width, interpolation = "nearest")(branchx_right_conv_block)
concat = tf.keras.layers.concatenate()([resize, ])


branchx_right_mul
branchy



