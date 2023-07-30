In this traffic problem, using varoius levels of Convolution layer, Max-pooling, various units of hidden layers can change our accurace. First of all, one Max-pooling and one Convolution Layer wiht one hidden layer of 128 units generated 95.44% acccuracy. Then without any hidden layer, we got 99.22% accuracy. 
Moreover adding two hidden layers of 1024 units generated 96.97% accuracy. After that, removing one hidden layer boosted up the accuracy to 98.61% . 

So, adding more units in a hidden layer can increase the accuracy, but adding more unit demands more time, then it takes longer time to generate the model. 

On the other hand, adding more hidden layers dropped the accuracy. Maybe it's because overfitting.
