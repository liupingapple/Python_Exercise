from keras import backend as K
from keras.engine.topology import Layer
import numpy as np

import tensorflow as tf

# from keras.activations import linear

class Dense_New(Layer):

    def __init__(self, units,
#                 activation=None,
                 use_bias=True,
#                 kernel_initializer='glorot_uniform',
#                 bias_initializer='zeros',
#                 kernel_regularizer=None,
#                 bias_regularizer=None,
#                 activity_regularizer=None,
#                 kernel_constraint=None,
#                 bias_constraint=None,
                 **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(Dense_New, self).__init__(**kwargs)
        self.units = units
#        self.activation = activations.get(activation)
        self.use_bias = use_bias
#        self.kernel_initializer = initializers.get(kernel_initializer)
#        self.bias_initializer = initializers.get(bias_initializer)
#        self.kernel_regularizer = regularizers.get(kernel_regularizer)
#        self.bias_regularizer = regularizers.get(bias_regularizer)
#        self.activity_regularizer = regularizers.get(activity_regularizer)
#        self.kernel_constraint = constraints.get(kernel_constraint)
#        self.bias_constraint = constraints.get(bias_constraint)
#        self.input_spec = InputSpec(min_ndim=2)
        self.supports_masking = True

    def build(self, input_shape):
        assert len(input_shape) >= 2
        input_dim = input_shape[-1]
        assert input_dim == self.units   #输入维度必须等于输出维度
        #记录用于局部连接的矩阵
        self.mask = K.variable(np.triu(np.ones((input_dim,input_dim))))

        self.kernel = self.add_weight(shape=(input_dim, self.units),
                                      initializer='glorot_uniform',
                                      name='kernel')
#                                      regularizer=self.kernel_regularizer,
#                                      constraint=self.kernel_constraint)
        if self.use_bias:
            self.bias = self.add_weight(shape=(self.units,),
                                        initializer='glorot_uniform',
                                        name='bias')
#                                        regularizer=self.bias_regularizer,
#                                        constraint=self.bias_constraint)
        else:
            self.bias = None
#        self.input_spec = InputSpec(min_ndim=2, axes={-1: input_dim})
        super(Dense_New, self).build(input_shape)
#        self.built = True

    def call(self, inputs):
        output = K.dot(inputs, tf.multiply(self.kernel,self.mask))
        if self.use_bias:
            output = K.bias_add(output, self.bias)
#        if self.activation is not None:
#            output = self.activation(output)
        return output

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = self.units
        return tuple(output_shape)

    def get_config(self):
        config = {
            'units': self.units,
#            'activation': activations.serialize(self.activation),
            'use_bias': self.use_bias
#            'kernel_initializer': initializers.serialize(self.kernel_initializer),
#            'bias_initializer': initializers.serialize(self.bias_initializer),
#            'kernel_regularizer': regularizers.serialize(self.kernel_regularizer),
#            'bias_regularizer': regularizers.serialize(self.bias_regularizer),
#            'activity_regularizer': regularizers.serialize(self.activity_regularizer),
#            'kernel_constraint': constraints.serialize(self.kernel_constraint),
#            'bias_constraint': constraints.serialize(self.bias_constraint)
        }
        base_config = super(Dense_New, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
