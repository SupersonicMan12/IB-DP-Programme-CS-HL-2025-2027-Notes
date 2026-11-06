## A4.1

> [!IB Style Question] Question 1
> Identify **two** differences between supervised learning and unsupervised learning. **[2]**

- Supervised learning uses labeled data
- Supervised learning predicts a known output label, while unsupervised learning finds hidden patterns or structure
- Supervised accuracy can be measured against known correct answers, unsupervised learning has no "standard answer"

> [!IB Style Question] Question 2
> A hospital wants to build a system that detects tumours in X-ray images. It has only a small set of labelled X-ray scans.
>
> Explain why transfer learning would be a suitable approach in this situation. **[4]**

What happens:
- Reuses a model pre-trained on another task (1)
- Fine-tuned using small labeled X-ray dataset (1)
Why:
- The pre-trained model has already learned general visual features such as edges, shapes and textures, carrying those over to X-rays (1)
- It therefore needs much less labeled data, decreasing training time and cost, while less likely overfitting (1)

> [!IB Style Question] Question 3
> A smartphone maker wants to add face-unlock to its phones.
>
> Compare and contrast running the face-recognition model on an edge device (the phone) with running it on a cloud-based platform. **[4]**

Disadvantages:
- Edge works offline and doesn't depend on a server
- Privacy: face data stays on the device
- Latency: edge is real-time
Advantages:
- Cloud has more compute, larger and more accurate models
Same:
- Trained model, same function of authenticating


> [!IB Style Question] Question 4
> A supermarket chain collects data on every customer transaction at its checkouts.
>
> **(a)** State the type of machine learning that would be used to discover which products are frequently bought together. **[1]**
>
> **(b)** Outline one reason this type of machine learning does not require labelled data. **[2]**
>
> **(c)** Describe how the results of this analysis could be used by the supermarket. **[2]**

a) Unsupervised Learning
b) the goal is pattern recognition, so there is no standard answer to be trained for
c) the results of this analysis could be used to improve customer experience, for instance, placing items bought with high association physically close

> [!IB Style Question] Question 5
> A delivery company is developing an autonomous drone that navigates through a city to drop off parcels.
>
> **(a)** Identify one feature of reinforcement learning (RL). **[1]**
>
> **(b)** Justify why reinforcement learning (RL) would be used to train the drone's navigation instead of supervised learning (SL). **[3]**
>
> **(c)** Outline one reason the drone should process its navigation decisions on an edge device rather than on a cloud-based platform. **[2]**

a) Positive reward to encourage a certain action
b) The environment is dynamic and needs continuous, sequential decisions. Impossible to provide a labeled dataset for every possible situation. RL learns by trial and error, rewarding for safe, fast delivery and penalties for collisions.
c) edge device offers far less latency, suitable for real-time response; edge device is also independent of a server, making the device self-contained

> [!IB Style Question] Question 6
> A technology start-up is training a large language model (LLM) for customer-service chatbots.
>
> **(a)** State one reason a standard laptop is unsuitable for training this model. **[1]**
>
> **(b)** Outline one difference between a tensor processing unit (TPU) and a graphics processing unit (GPU). **[2]**
>
> **(c)** Describe one advantage and one disadvantage for the start-up of training the model on a cloud-based platform rather than buying its own hardware. **[4]**

a) insufficient computational power
b) TPU is specialized for neural network learning (an instance of ASIC, by Google), while GPU is specialized for large amounts of parallel computations, which can also be useful for machine learning but is less specialized.
c) advantage: a start-up does not necessarily have enough resources or capital to build its own data-center, which is costly; in the early stages, a start-up needs to be build prototypes with least cost. disadvantage: a start-up trusts another organization with their information, potentially losing user privacy and making their services dependent on another organization, with greater latency and unreliableness

## A4.2

> [!IB Style Question] Question 7
> A bank is training a machine learning model to predict whether loan applicants will repay their loans. The dataset contains customer records collected from several branches over ten years.
>
> **(a)** Identify **two** examples of data quality problems that may be present in this dataset. **[2]**
>
> **(b)** Outline why duplicate records should be removed before training the model. **[2]**
>
> **(c)** Some records are missing values for "annual income". Describe **one** advantage and **one** disadvantage of using imputation to deal with the missing values. **[4]**

a) duplicate records and inconsistent format
b) duplicate records can count the same record multiple times, leading to unintentional, unequal weights that decrease the accuracy of the model.
c) 
- Record is retained -> other features' information kept, dataset size preserved
- Imputed values may not reflect true values -> distorts distribution, reduces variance, model learns false patterns.

> [!IB Style Question] Question 8
> A fitness app collects data from users, including age (in years), daily step count, and resting heart rate (in beats per minute). The data will be used to train a k-nearest neighbours (k-NN) model.
>
> **(a)** State the purpose of normalization. **[1]**
>
> **(b)** Explain why the features should be normalized or standardized before training a k-NN model. **[3]**
>
> **(c)** Some users have recorded extremely high step counts due to a sensor fault. Outline why standardization may be preferred over normalization in this situation. **[2]**

a) to rescale values to a fixed range, typically 0 to 1
b) normalization allows all dimensions to have equal weight, so that no variable dominates the others and misleads the model. for example, daily step count can go above 10000, while age is usually within 100; then calculating the distance would mostly depend on daily step count.
c) standardization is less prone to outliers because it is based on the mean, while normalization establishes the range through minimum and maximum, which would be greatly affected by an outlier.

> [!IB Style Question] Question 9
> An online retailer has a dataset with 120 features describing each customer's browsing behaviour. It wants to predict which customers are likely to stop using the website.
>
> **(a)** Define the term *feature selection*. **[1]**
>
> **(b)** Outline **two** benefits of performing feature selection on this dataset. **[4]**
>
> **(c)** Distinguish between a filter method and a wrapper method of feature selection. **[3]**

a) feature selection is the choosing of features that together perform the best prediction
b) ==Feature selection reduces the number of dimensions, reducing overfitting, which is important because irrelevant features add noise the model may learn. The result is a model that generalizes better to new customers==. It also reduces the amount of computational power and time necessary, as there are fewer dimensions to consider and evaluate, removing less relevant variables.
c) a filter evaluates the variables independently and statistically (such as correlation with the output), then selects the best subset; a wrapper method takes subsets from the variables, tries many of them and chooses the best-performing subset. The latter is more time-expensive.

> [!IB Style Question] Question 10
> A research team is analysing genetic data. Each sample contains measurements for 20 000 genes, but only 300 patient samples are available.
>
> **(a)** Identify **one** consequence of the curse of dimensionality for this dataset. **[1]**
>
> **(b)** Explain why distance-based algorithms, such as k-means clustering, become less effective as the number of dimensions increases. **[3]**
>
> **(c)** Describe how dimensionality reduction could improve the model developed by the research team. **[3]**

a) the data points become overly sparse in the space of 20000-dimensions
b) less relevant dimensions contribute equally to the distance. all points become similarly distant. this means that centroids stop meaning anything, as the cluster assignments by distance are arbitrary.
c) Reduces noise to make more accurate; less memory and computation; preserving relevant information allows the model to generalize; visualize

Summary of advantages:
- Reduce noise, to generalize better
- Less memory and computation
- Visualize

## A4.3 

> [!IB Style Question] Question 11 — A4.3.1 Linear regression
> An estate agent uses linear regression to predict house prices (in $1000s$) from floor area (in m²). The model produced is:
> $$\hat y = 2.5x + 40$$
> with $r^2 = 0.81$.
>
> **(a)** Identify the dependent variable in this model. **[1]**
>
> **(b)** Calculate the predicted price of a house with a floor area of 120 m². **[1]**
>
> **(c)** Outline the meaning of the slope in the context of this model. **[2]**
>
> **(d)** Explain what the value $r^2 = 0.81$ indicates about the model. **[2]**
>
> **(e)** Outline **one** reason the model may give an unreliable prediction for a house with a floor area of 900 m². **[2]**

a) the dependent variable is the house price
b) $\hat y = 2.5 \cdot 120 + 40 = 340$ thousand
c) the slope means the amount of increase of house price in 1000s per 1m^2 increase in floor area; here, 2.5 slope means that the house price increases by 2500 per 1m^2 increase in floor area
d) $r^2$ is the coefficient of determination. It means 81% of the variation in house price is explained by floor area in this linear model.
The coefficient of correlation $r$ is 0.9, which is positive, because house price increases with floor area. **OR** the other 19% is due to factors like location that the linear model does not consider.
e) One reason is that the real house prices may not be linear with respect to floor area. A linear regression assumes a linear correlation and may deviate from reality for large floor area values.

> [!IB Style Question] Question 12 — A4.3.2 Classification
> A hospital wants to use a decision tree to help doctors diagnose a disease based on patients' symptoms.
>
> **(a)** State the purpose of a leaf node in a decision tree. **[1]**
>
> **(b)** Outline **one** reason a decision tree is suitable for medical diagnosis. **[2]**
>
> An online streaming service uses k-nearest neighbours (k-NN) to recommend films to users through collaborative filtering.
>
> **(c)** Describe how k-NN could be used to recommend a film to a user. **[3]**
>
> **(d)** Outline the effect of choosing a very small value of $k$. **[2]**

a) A leaf node denotes a conclusion, the final desired result
b) the doctor can follow the path from the root to the leaf and see exactly which symptoms led to the diagnosis. the doctor can check the decision, justify it to the patient and spot mistakes. This matters because medical decisions are high-stakes and doctors are accountable for them.
c) Represent each user as a vector of their film ratings or viewing history. Use a distance or similarity measure to find the k users most similar to the target user. Recommend films those neighbors rated highly that the target user hasn't watched yet, e.g. by a majority vote or average rating.
d) The recommendation depends on only one or a few neighbors. So it is **sensitive to noise and outliers**. One user with unusual taste can skew the result, which leads to **overfitting** and unstable recommendations.

> [!IB Style Question] Question 13 — A4.3.3 Hyperparameter tuning and evaluation
> A model is developed to screen patients for a rare cancer. When tested on 200 patients, the results were:
>
> |              | Predicted positive | Predicted negative |
> | ------------ | ------------------ | ------------------ |
> | **Actual positive** | 15          | 5                  |
> | **Actual negative** | 20          | 160                |
>
> **(a)** Calculate the accuracy of the model. **[1]**
>
> **(b)** Calculate the recall of the model. **[1]**
>
> **(c)** Justify whether precision or recall should be prioritised for this model. **[3]**
>
> **(d)** Distinguish between a parameter and a hyperparameter. **[2]**
>
> **(e)** The model achieves 99% accuracy on the training data but 70% on the test data. Explain what this suggests and how hyperparameter tuning could address it. **[3]**

a) accuracy = (15+160)/200 = 0.875 = 87.5%
b) recall = (TP)/(Actual positive) = 75%
c) recall should be prioritized, because false negative is more costly: it would mean that the cancer patient remains unaware of the disease, leading to a later discovery. On the other hand, a false positive leads to anxiety and rechecks, which is an acceptable price compared to a false negative.
d) parameters can be learned from the training data, hyperparameters is determined before the model runs manually and would determine the entire architecture
e) Overfitting has occurred: it has adapted strongly to the training data set but fails to generalize. For example, the hyperparameter of depth can be set as too large, leading to overfitting of the model. One can reduce the hyperparameter and test different values to find the optimal value.

> [!IB Style Question] Question 14 — A4.3.4 Clustering
> A clothing retailer wants to segment its customers based on purchasing data, such as annual spending and number of visits per year.
>
> **(a)** State why clustering is an example of unsupervised learning. **[1]**
>
> **(b)** Describe how the k-means algorithm groups the customers into clusters. **[4]**
>
> **(c)** Outline **one** limitation of the k-means algorithm. **[2]**
>
> **(d)** Describe how the retailer could use the resulting clusters. **[2]**

a) clustering is unsupervised learning because it recognizes patterns that are not previously labeled or discovered
b) k-means algorithm first chooses k different centroids among the records, then it groups each record with its closest point by some similarity measure. All groups calculate their new centroids, and that leads to another round of grouping. When the result converges, k desired groups are formed.
c) k-means is highly dependent on the initial seed of k, sometimes that k is not known or hard to test for, requiring manual, human discretion.
d)  a retailer can use clustering to understand the preferences of customers: each customer record is a vector of their preferences for different products, clustering identifies groups of customers with similar preferences. This similar preference can lead to better recommendations and hence better sales

> [!IB Style Question] Question 15 — A4.3.5 Association rules
> A police department analyses data from 200 neighbourhoods. 50 neighbourhoods report vandalism, 80 report theft, and 40 report both vandalism and theft.
>
> **(a)** Calculate the support for {vandalism, theft}. **[1]**
>
> **(b)** Calculate the confidence of the rule vandalism ⇒ theft. **[1]**
>
> **(c)** Calculate the lift of the rule vandalism ⇒ theft. **[2]**
>
> **(d)** Interpret the lift value in the context of this scenario, and outline how the police could use this result. **[3]**

a) support = 40/200 = 0.2
b) 40/50 = 0.8
c) lift = 0.8/0.4 = 2.0
d) The likelihood of there being theft when vandalism is given is 80%, while the likelihood of there being theft in general is 40%. This ratio is > 1, meaning that the vandalism and theft has positive association: knowing vandalism increases the chances of having theft twice. The police could use this positive association to send more police to areas with greater vandalism to prevent theft.

> [!IB Style Question] Question 16 — A4.3.6 Reinforcement learning
> A warehouse uses a robot that learns to pick and move packages using reinforcement learning (RL).
>
> **(a)** Define the term *policy* in reinforcement learning. **[1]**
>
> **(b)** Describe how the robot (agent) interacts with its environment to learn, referring to states, actions and rewards. **[4]**
>
> **(c)** Explain the exploration versus exploitation trade-off in the context of the robot. **[3]**

a) policy is the decision-rules of the robot: it is a mapping from state to action
b) the robot starts with a state, or situation of the environment and itself. According to its policy, it chooses an action to perform. The environment moves into a different state and gives a positive or negative reward, signaling the robot whether they did a good job. The robot updates its policy so that it is more likely to receive reward. This process is iterated repeatedly to maximize cumulative reward over time.
c) For the robot, exploitation means always using the route it already knows works. Exploration means sometimes trying a different aisle that might turn out to be quicker. If it only exploits, it may never find the shortest route; if it only explores, it wastes time on slower routes. So it should balance between the two: explore more in the start and exploit more in the long run.

> [!IB Style Question] Question 17 — A4.3.7 Genetic algorithms
> A courier company uses a genetic algorithm to find the shortest route for a driver visiting 30 delivery locations (a travelling salesperson problem).
>
> **(a)** State what a single member of the population represents in this scenario. **[1]**
>
> **(b)** Outline a suitable fitness function for this problem. **[2]**
>
> **(c)** Describe the role of crossover and mutation in producing the next generation. **[4]**
>
> **(d)** Identify **two** possible termination conditions for the algorithm. **[2]**

a) a single member of the population represents a possible route for the 30-location visit
b) 
- Fitness is based on the total distance of the route
- Shorter routes are fitter, e.g. fitness = 1 / total distance
c) 
- crossover takes a segment of the route from one parent and fills the remaining locations in the order they appear in the second. The child inherits the good sections of route from both parents
- mutation makes a small random change, e.g. swap the positions of two locations. This keep the population diverse and stops the algorithm from getting stuck in a **local optimal.**
d) two of the following:
- a maximum number of generations has been reached, or a time or computation limit has been reached
- a fitness threshold has been reached: the solution is sufficiency good
- there has been no improvement in the best fitness, the program is stuck

> [!IB Style Question] Question 18 — A4.3.8 Artificial neural networks
> **(a)** Draw a labelled diagram of a single perceptron, showing its inputs, weights, bias, activation function and output. **[4]**
>
> **(b)** Outline the role of the activation function in a neural network. **[2]**
>
> **(c)** Explain why a multi-layer perceptron (MLP) can model more complex patterns than a single perceptron. **[3]**

a) ![[Screenshot 2026-11-05 at 14.50.38.png]]

inputs are x1 and x2, weights are w1 and w2, bias is b, activation function converts the linear combination + bias into the perceptron's own output value.

b) 
- decides the neuron's output: it chooses to squash the output into a useful range and whether or how strongly it fires
- introduces non-linearity: without it, multiple layers would simply be a linear combination overall

c) ==marked as not-a-great-question==
1. A single perceptron can only draw a linear decision boundary, it cannot solve problems that aren't linearly separable
2. An MLP has hidden layers. Each neuron in the hidden layer learns a simple feature, later layers combine those features gradually into more complex ones
3. Because each layer applies a non-linear activation, the network as a whole becomes a non-linear function. With enough layers, complex decisions can be made.

> [!IB Style Question] Question 19 — A4.3.9 Convolutional neural networks
> A farm uses a convolutional neural network (CNN) to identify diseased crops from photographs of leaves.
>
> **(a)** State the purpose of a pooling layer. **[1]**
>
> **(b)** Describe how a convolutional layer processes an input image. **[3]**
>
> **(c)** Outline the effect of increasing the stride of a convolutional layer. **[2]**
>
> **(d)** Explain how a CNN learns a spatial hierarchy of features to classify the leaf images. **[3]**

a) Pooling downsamples the feature maps, reducing their size and computation needed.
b) Feature map is the resultant of scanning the kernel over different positions of an image: each entry in the resulting matrix is the by-term product sum of the kernel and the sub-matrix. This convolutional layer is then fed into further neural networks to do complex identification.
c) stride is the amount of spacing between different sampling positions. larger stride leads to a smaller convolutional layer, saving memory and space. it can also lose resolution or information.
d) it starts by identifying simpler features like vertical and horizontal edges and color; then goes to middle layers of textures, shapes e.g. spots, lesions, vein patterns; then goes to deep layers: whole patterns of disease on the leaf.

> [!IB Style Question] Question 20 — A4.3.10 Model selection and comparison
> A bank needs a model to decide whether to approve loan applications. It is considering a decision tree and a deep neural network.
>
> **(a)** Outline **one** reason different algorithms can produce different results on the same dataset. **[2]**
>
> **(b)** Discuss which model the bank should select, considering the nature of the problem and the desired outcomes. **[6]**

