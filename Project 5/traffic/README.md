# CS50AI Project 5 - Traffic

## Experimentation

First Convolutional neural network:
I started off by creating a convolutional neural network with one 32-filter convolutional layer and one pooling layer leading into a 128-neuron hidden layer with 20% Dropout which in turn led into the output layer.

This resulted in: loss: 0.9663 - accuracy: 0.7101

Second Convolutional neural network:
I added a second convolutional and pooling layer before the flatten step.

This resulted in: loss: 0.1286 - accuracy: 0.9701, with each epoch completing in a few ms less.

Third Convolutional neural network:
I added a 20% dropout before the second convolutional layer.

This resulted in: loss: 0.2497 - accuracy: 0.9360, not as good metrics but a model that may work better due to less overfitting.

Fourth Convolutional neural network:
I changed the second convolutional layer to a 64-filter layer.

This resulted in: loss: 0.1352 - accuracy: 0.9684, better metrics though the time taken per epoch went up by ~40%

Fifth Convolutional neural network:
I changed the final dropout to 50%.

This resulted in: loss: 3.5017 - accuracy: 0.0542, creating a model of little use

Sixth Convolutional neural network:
I swapped the dropout values - changing the 20% dropout before the second convolutional layer to 50% and changing back the final dropout to 20%.

This resulted in: loss: 1.7671 - accuracy: 0.4283

Seventh Convolutional neural network:
I reverted to the 4th network and added another 20% dropout layer, and another 64-filter convolutional layer and max-pooling layer.

This resulted in: loss: 0.1206 - accuracy: 0.9688, working well but complicated.

Eighth Convolutional neural network:
I changed the 64-filter layers to 32-filter layers.

This resulted in: loss: 0.2287 - accuracy: 0.9310, faster but not as good.

### End Result

The best attempt of the above was the Fourth Convolutional neural network with a good model for the dataset with subsequent networks becoming more complicated with varying effects. Hence, I used the fourth version as the final network.
