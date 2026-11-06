## A4.1

**Question 1** _(2 marks)_  
**Identify** two differences between supervised learning and unsupervised learning.
- Supervised learning uses labeled data
- Supervised learning predicts a known output label, while unsupervised learning finds hidden patterns or structure
- Supervised accuracy can be measured against known correct answers, unsupervised learning has no "standard answer"

**Question 2** _(4 marks)_  
A hospital wants to build a system that detects tumours in X-ray images. It has only a small set of labelled X-ray scans.  
**Explain** why transfer learning would be a suitable approach in this situation.

What happens:
- Reuses a model pre-trained on another task (1)
- Fine-tuned using small labeled X-ray dataset (1)
Why:
- The pre-trained model has already learned general visual features such as edges, shapes and textures, carrying those over to X-rays (1)
- It therefore needs much less labeled data, decreasing training time and cost, while less likely overfitting (1)

**Question 3** _(4 marks)_  
A smartphone maker wants to add face-unlock to its phones.  
**Compare and contrast** running the face-recognition model on an edge device (the phone) with running it on a cloud-based platform.

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
b) medical diagnosis is a complicated task involving many cases and conditions that must be considered. A decision tree can systematize the decision-making, taking these cases into consideration
c) k-NN is an unsupervised learning method that clusters data points without prelabeled data. It can cluster users of similar preferences together, suggesting that they are likely to prefer the same films. Then, recommendations for a user can be based on what users in their clusters like.
d) an overly small value of $k$ assumes a smaller number of groups. The groups may be too broad, grouping records that are actually not similar with each other and becoming less effective.

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

> [!IB Style Question] Question 16 — A4.3.6 Reinforcement learning
> A warehouse uses a robot that learns to pick and move packages using reinforcement learning (RL).
>
> **(a)** Define the term *policy* in reinforcement learning. **[1]**
>
> **(b)** Describe how the robot (agent) interacts with its environment to learn, referring to states, actions and rewards. **[4]**
>
> **(c)** Explain the exploration versus exploitation trade-off in the context of the robot. **[3]**

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

> [!IB Style Question] Question 18 — A4.3.8 Artificial neural networks
> **(a)** Draw a labelled diagram of a single perceptron, showing its inputs, weights, bias, activation function and output. **[4]**
>
> **(b)** Outline the role of the activation function in a neural network. **[2]**
>
> **(c)** Explain why a multi-layer perceptron (MLP) can model more complex patterns than a single perceptron. **[3]**

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

> [!IB Style Question] Question 20 — A4.3.10 Model selection and comparison
> A bank needs a model to decide whether to approve loan applications. It is considering a decision tree and a deep neural network.
>
> **(a)** Outline **one** reason different algorithms can produce different results on the same dataset. **[2]**
>
> **(b)** Discuss which model the bank should select, considering the nature of the problem and the desired outcomes. **[6]**