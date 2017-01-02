# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
from environment.environment import Environment
from projection.vae_projection import VAEProjection
from ec.qec_table import QECTable
from agent.agent import EpisodicControlAgent

k = 50
knn_capacity = 100000
observation_dim = 84 * 84
state_dim = 64
gamma = 0.99
epsilon = 0.005
vae_train_step_size = 400000
vae_train_batch_size = 100




num_actions = Environment.get_action_size()
environment = Environment.create_environment()

projection = VAEProjection()

qec_table = QECTable(projection, state_dim, num_actions, k, knn_capacity)

agent = EpisodicControlAgent(environment, qec_table, num_actions, gamma, epsilon)

# Session should be started after Lab environment is created. (To run Lab with GPU)
sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)

projection.set_session(sess)

# Train VAE
projection.train(sess, environment, vae_train_step_size, vae_train_batch_size)


for i in range(1):
  ret = agent.step()
  if ret != None:
    print(ret)
