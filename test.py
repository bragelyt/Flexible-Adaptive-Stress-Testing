import json
from models.actor import NeuralActor


def main():
    with open('nnParameters.json') as f:
        parameters = json.load(f)
    learningRate = parameters['anet_learning_rate']
    activationFunction = parameters['anet_activation_function']
    outputActivationFunction = parameters['output_activation_function']
    optimizer = parameters['anet_optimizer']
    convLayersDim = parameters['anet_conv_layers_and_neurons_per_layer']
    denseLayersDim = parameters['anet_dense_layers_and_neurons_per_layer']
    lossFunction = parameters['loss_function']

    NA  = NeuralActor(
            input_size = 2,
            output_size = 2,
            learningRate = learningRate,
            optimizer = optimizer,
            activation = activationFunction,
            lossFunciton = lossFunction,
        )
    print(NA.getPrediction([1.,1.]))
    print(NA.getPrediction([0.,1.]))
    NA.trainOnBatch([[[1.,1.],[0.5, 0.5]],
                     [[0.,1.],[0.8, 0.2]]])
    print(NA.getPrediction([1.,1.]))
    print(NA.getPrediction([0.,1.]))

    
if __name__ == "__main__":
    main()