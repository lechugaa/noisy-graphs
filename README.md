# Graph Privacy

## Summary 

Advances in graph theory and the increase in available computing power have allowed the study and simulation of complex
systems that were previously out of technological reach. Despite the various benefits that this has brought to society,
it has also violated the privacy of populations since the (no longer so) complex social networks in which we live are
the perfect case study for graph theory aided by the great capacity for data mining provided by current technology.

Although there is previous research on the topic of privacy in networks, the issue of guaranteeing privacy even from the
network-generating organism has not been adequately studied.

This paper presents a mechanism for the construction of graphs, called \textit{noisy graphs}, that allows maintaining
the privacy of the connections between vertices through the introduction of fake edges at all times during the
construction. The proposed mechanism performs the construction through the individual collection of the neighbor lists
of each vertex of the system and introduces noise to the graph so that at no moment there is complete certainty of the
edges of the graph, even while it is being generated.

Experimentally, this work employs random graphs generated according to the preferential attachment model of Barabási and
Albert since, to the present day, it is the model that best models naturally occurring networks.

To measure the uncertainty added by the proposed algorithm, a metric derived from Shannon's entropy is used to quantify
the number of bits of information that the graph owner must obtain to know, with absolute certainty, the list of real
edges of a given vertex.

Finally, the proposed algorithm aims for noisy graphs to have the same utility as a graph that exactly represents the
modeled system in terms of the relative importance of the vertices with respect to their values of degree, eigenvector,
closeness, and betweenness centralities. To quantify this utility, this paper calculates the Spearman's rank correlation
coefficient on the ordering of the vertices, with respect to the previously mentioned centrality metrics, between the
noisy graph and a traditional graph without uncertainty.

[Link to the full thesis](https://github.com/lechugaa/noisy-graphs/blob/master/thesis.pdf)

## Configuration

### Python and Requirements

This project was developed using python 3.9.7. In the root directory there is a file called `requirements.txt` that
contains all the necessary dependencies to run the code. To install them, use the following command:

```
pip install -r requirements.txt
```
