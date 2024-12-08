import nn



class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    NO ES CLASIFICACION, ES REGRESION. ES DECIR; APRENDER UNA FUNCION.
    SI ME DAN X TENGO QUE APRENDER A OBTENER LA MISMA Y QUE EN LA FUNCION ORIGINAL DE LA QUE QUIERO APRENDER
    """
    def __init__(self):
        # Initialize your model parameters here
        # For example:
        # self.batch_size = 20
        # self.w0 = nn.Parameter(1, 5)
        # self.b0 = nn.Parameter(1, 5)
        # self.w1 = nn.Parameter(5, 1)
        # self.b1 = nn.Parameter(1, 1)
        # self.lr = -0.01
        #
        "*** YOUR CODE HERE ***"
        
        # Inicialización de la red neuronal 
        # La primera es 1 porque se introduce el valor de x para predecir el nodo
        # Primer param --> numEntradas 
        # Segundo param --> numNeuronas --> 1 BIAS por neurona

        self.batch_size = 1 # Cuantos valores analiza a la vez
        self.w0 = nn.Parameter(1, 50)
        self.b0 = nn.Parameter(1, 50)
        self.w1 = nn.Parameter(50, 1)
        self.b1 = nn.Parameter(1, 1)

        # self.w0 = nn.Parameter(1, 5)
        # self.b0 = nn.Parameter(1, 5)
        # self.w1 = nn.Parameter(5, 1)
        # self.b1 = nn.Parameter(1, 1)

        self.lr = -0.01


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1). En este caso cada ejemplo solo esta compuesto por un rasgo
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values.
            Como es un modelo de regresion, cada valor y tambien tendra un unico valor
        """
        "*** YOUR CODE HERE ***"

        # Calcula el valor pred del seno

        prod0 = nn.Linear(x, self.w0) # Multiplica la matriz de pesos por la entrada
        add_bias0 = nn.AddBias(prod0, self.b0) #Añade el bias
        capa_esc = nn.ReLU(add_bias0) #Calcula el seno de la salida
        prod1= nn.Linear(capa_esc, self.w1) # Multiplica la matriz de pesos por la entrada
        add_bias1 = nn.AddBias(prod1, self.b1) #Añade el bias
        return add_bias1 # No introducimos la ReLU al final porque solo devuelve valores positivos


    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
                ----> ES FACIL COPIA Y PEGA ESTO Y ANNADE LA VARIABLE QUE HACE FALTA PARA CALCULAR EL ERROR 
                return nn.SquareLoss(self.run(x),ANNADE LA VARIABLE QUE ES NECESARIA AQUI), para medir el error, necesitas comparar el resultado de tu prediccion con .... que?
        """
        "*** YOUR CODE HERE ***"

        # Error cometido, lo calcula con mean square error --> Regression Problem

        predicted_value = self.run(x)

        return nn.SquareLoss(predicted_value, y)


    def train(self, dataset):
        """
        Trains the model.
        
        """
        
        batch_size = self.batch_size
        total_loss = 100000
        while total_loss > 0.02:
            #ITERAR SOBRE EL TRAIN EN LOTES MARCADOS POR EL BATCH SIZE COMO HABEIS HECHO EN LOS OTROS EJERCICIOS
            #ACTUALIZAR LOS PESOS EN BASE AL ERROR loss = self.get_loss(x, y) QUE RECORDAD QUE GENERA
            #UNA FUNCION DE LA LA CUAL SE  PUEDE CALCULAR LA DERIVADA (GRADIENTE)

            "*** YOUR CODE HERE ***"

            for x, y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x,y)

                gradients = nn.gradients(loss, [self.w0, self.b0, self.w1, self.b1]) # Calcula el gradiente de la loss de los pesos y el bias

                self.w0.update(gradients[0], self.lr) # update es el peso actual - gradiente*learning rate
                self.b0.update(gradients[1], self.lr) 
                self.w1.update(gradients[2], self.lr)
                self.b1.update(gradients[3], self.lr)

                new_loss = self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))
            
            total_loss = nn.as_scalar(new_loss) # Transforma la pérdida en un float de python

            
class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        # TEN ENCUENTA QUE TIENES 10 CLASES, ASI QUE LA ULTIMA CAPA TENDRA UNA SALIDA DE 10 VALORES,
        # UN VALOR POR CADA CLASE

        output_size = 10 # TAMANO EQUIVALENTE AL NUMERO DE CLASES DADO QUE QUIERES OBTENER 10 CLASES
        pixel_dim_size = 28
        pixel_vector_length = pixel_dim_size* pixel_dim_size
 
        "*** YOUR CODE HERE ***"

        self.batch_size = 10

        self.w0 = nn.Parameter(pixel_vector_length, 300)
        self.b0 = nn.Parameter(1, 300)
        self.w1 = nn.Parameter(300, 100)
        self.b1 = nn.Parameter(1, 100)
        self.w2 = nn.Parameter(100, 50)
        self.b2 = nn.Parameter(1, 50)
        self.w3 = nn.Parameter(50, output_size)
        self.b3 = nn.Parameter(1, output_size)
        self.lr = -0.01

        # VERSIÓN 1
        """
        self.w0 = nn.Parameter(pixel_vector_length, 300)
        self.b0 = nn.Parameter(1, 300)
        self.w1 = nn.Parameter(300, 100)
        self.b1 = nn.Parameter(1, 100)
        self.w2 = nn.Parameter(100, output_size)
        self.b2 = nn.Parameter(1, output_size)
        """

     

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
            output_size = 10 # TAMANO EQUIVALENTE AL NUMERO DE CLASES DADO QUE QUIERES OBTENER 10 "COSENOS"
        """
        "*** YOUR CODE HERE ***"

        prod0 = nn.Linear(x, self.w0) # Multiplica la matriz de pesos por la entrada
        add_bias0 = nn.AddBias(prod0, self.b0) #Añade el bias
        capa_esc0 = nn.ReLU(add_bias0) #Calcula el seno de la salida
        prod1= nn.Linear(capa_esc0, self.w1) # Multiplica la matriz de pesos por la entrada
        add_bias1 = nn.AddBias(prod1, self.b1) #Añade el bias
        capa_esc1 = nn.ReLU(add_bias1)
        prod2 = nn.Linear(capa_esc1, self.w2)
        add_bias2 = nn.AddBias(prod2, self.b2)
        capa_esc2 = nn.ReLU(add_bias2)
        prod3 = nn.Linear(capa_esc2, self.w3)
        add_bias3 = nn.AddBias(prod3, self.b3)
        return add_bias3 # No introducimos la ReLu al final porque solo predice valores
    
        # VERSIÓN 1

        """
        prod0 = nn.Linear(x, self.w0) # Multiplica la matriz de pesos por la entrada
        add_bias0 = nn.AddBias(prod0, self.b0) #Añade el bias
        capa_esc0 = nn.ReLU(add_bias0) #Calcula el seno de la salida
        prod1= nn.Linear(capa_esc0, self.w1) # Multiplica la matriz de pesos por la entrada
        add_bias1 = nn.AddBias(prod1, self.b1) #Añade el bias
        capa_esc1 = nn.ReLU(add_bias1)
        prod2 = nn.Linear(capa_esc1, self.w2)
        add_bias2 = nn.AddBias(prod2, self.b2)
        """

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).
        POR EJEMPLO: [0,0,0,0,0,1,0,0,0,0,0] seria la y correspondiente al 5
                     [0,1,0,0,0,0,0,0,0,0,0] seria la y correspondiente al 1

        EN ESTE CASO ESTAMOS HABLANDO DE MULTICLASS, ASI QUE TIENES QUE CALCULAR 
        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"#NO ES NECESARIO QUE LO IMPLEMENTEIS, SE OS DA HECHO
        return nn.SoftmaxLoss(self.run(x), y) # COMO VEIS LLAMA AL RUN PARA OBTENER POR CADA BATCH
                                              # LOS 10 VALORES DEL "COSENO". TENIENDO EL Y REAL POR CADA EJEMPLO
                                              # APLICA SOFTMAX PARA CALCULAR LA PROBABILIDA MAX
                                              # Y ESA SERA SU PREDICCION,
                                              # LA CLASE QUE MUESTRE EL MAYOR PROBABILIDAD, LA PREDICCION MAS PROBABLE, Y LUEGO LA COMPARARA CON Y 

    def train(self, dataset):
        """
        Trains the model.
        EN ESTE CASO EN VEZ DE PARAR CUANDO EL ERROR SEA MENOR QUE UN VALOR O NO HAYA ERROR (CONVERGENCIA),
        SE PUEDE HACER ALGO SIMILAR QUE ES EN NUMERO DE ACIERTOS. EL VALIDATION ACCURACY
        NO LO TENEIS QUE IMPLEMENTAR, PERO SABED QUE EMPLEA EL RESULTADO DEL SOFTMAX PARA CALCULAR
        EL NUM DE EJEMPLOS DEL TRAIN QUE SE HAN CLASIFICADO CORRECTAMENTE 
        """
        batch_size = self.batch_size
        while dataset.get_validation_accuracy() < 0.97:
            #ITERAR SOBRE EL TRAIN EN LOTES MARCADOS POR EL BATCH SIZE COMO HABEIS HECHO EN LOS OTROS EJERCICIOS
            #ACTUALIZAR LOS PESOS EN BASE AL ERROR loss = self.get_loss(x, y) QUE RECORDAD QUE GENERA
            #UNA FUNCION DE LA LA CUAL SE  PUEDE CALCULAR LA DERIVADA (GRADIENTE)
            "*** YOUR CODE HERE ***"

            for x, y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x,y)

                gradients = nn.gradients(loss, [self.w0, self.b0, self.w1, self.b1, self.w2, self.b2, self.w3, self.b3]) # Calcula el gradiente de la loss de los pesos y el bias

                self.w0.update(gradients[0], self.lr) # update es el peso actual - gradiente*learning rate
                self.b0.update(gradients[1], self.lr) 
                self.w1.update(gradients[2], self.lr)
                self.b1.update(gradients[3], self.lr)
                self.w2.update(gradients[4], self.lr)
                self.b2.update(gradients[5], self.lr)
                self.w3.update(gradients[6], self.lr)
                self.b3.update(gradients[7], self.lr)

                # VERSIÓN 1
                """
                gradients = nn.gradients(loss, [self.w0, self.b0, self.w1, self.b1, self.w2, self.b2]) # Calcula el gradiente de la loss de los pesos y el bias

                self.w0.update(gradients[0], self.lr) # update es el peso actual + gradiente*learning rate
                self.b0.update(gradients[1], self.lr) 
                self.w1.update(gradients[2], self.lr)
                self.b1.update(gradients[3], self.lr)
                self.w2.update(gradients[4], self.lr)
                self.b2.update(gradients[5], self.lr)
                
                """
                #new_loss = self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))
            
            #total_loss = nn.as_scalar(new_loss) # Transforma la pérdida en un float de python







