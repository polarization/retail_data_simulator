# Motivation
As a retail data analyser or 3-rd AI product provider, we want to simulate 
the guest flow data and specific guest visiting data by given or randomly 
generated undirected graph (graph theory) of retail locations, so that we can:
* make big or huge volume data test
* get some common sense from location connectivity graph and related
  guest shopping routes
* simulate the basic ground truth of some statistic metrics which is
  meaningful for retailer
* simulate the AI product predictions by estimated/acceptable errors
* estimate statistic metrics errors by comparing ground truth and
  predictions to evaluate metrics' value to retailer

# Getting Start
So far, this tools can be used by two ways:
* Define retail site information by hand writing, you can base on small_expo
.py to setup your site, input all the properties' value and define vertex, 
edges, position-device mapping carefully, and run it:
`python3 small_expo.py`
A retail json data with the given building name would be generated:
small-expo.json, for instance.
* Imagine a big retail building which has many floors, atom district, lift, 
and escalators, only input properties' value and without defining vertex, 
edges, position-device mapping by hand. Run it:
`python3 shopping_mall.py`
A big retail json data with the given building name would be generated:
galaxy-tower.json, for instance.

You can run small_expo.py and shopping_mall.py many times to generate as 
many virtual building as you like.

Then you can generate truth data and prediction data as many times as you 
like. One day's data for every times' calling.
`python3 orchestrator.py --building_name=galaxy-tower-0 --date=2020-07-03`

# Basic Concept

### arena
retail site information, main parts of Arena listed below:
* connectivity graph: position as vertex, routes between position as edge,
  also contains edge's district ID, weights add-on, expectation, standard 
  deviation, minimum time cost of edge's. This graph is mainly used for ground
  ruth data generating. This graph must be connected graph.
* directed district logical graph: Directed hierarchical district graph,
  also contains edge's direction properties only between branch vertex and
  leaf vertex. This graph is mainly used for predicting district data.
  This graph must be directed acyclic graph.
* position-device mapping

### truth:
Ground Truth, big/huge amount of bugs which carry time currency crawl
in connectivity graph, pass by vertex and spend time currency in edges. 
Each bugs have some time currency, and the entrance time, position, the 
exit position also has been given. The time currency they cost is randomly 
determined by edge's expectation, standard  deviation, when a bug's time 
currency run out or location closing time reached, this bug need to find a 
simple way from its current position to its exit position and spend minimum 
time cost in each edge it would pass.

In this way, we can get each bug's path and timestamp it passed position.

### prediction:
Conditioned randomly sampling, determined by product's simulating, is from 
ground truth data, so we can get basic prediction data which can be used for
metrics.

# Basic Design
### config
contains retail site information, each building should have one module and 
have the same keys with different values

### data
contains files with data:
* truth_path.json: bug's truth path data in building
* truth_inout.json: ground truth of in-out data
* real_inout.json: in-out data provided by products
* truth_recognition.json: ground truth of recognition data
* real_recognition.json: recognition data provided by products

### entity:
Active entity in arena, so far only Bug and FaceBucket
* Bug, passenger simulation
* FaceBucket, face bucket for landscape view product, it contains some bugs,
  and other bugs is not in it. It also calculate:
    * threshold: best fit threshold if not given
    * pgc: probability of other bug is recognized as other bug
    * pvc: probability of a bug is recognized as itself
    * pvw: probability of a bug is recognized as another bug
    * pvm: probability of a bug is recognized as other bug

> You are all bugs. -- Three Body

### face_triple_data
triple pair of different face recognition algorithm

### metrics:
Contains lots of metrics and its statistical methods, compare with metrics 
from ground truth and prediction to error analysis.

### product:
AI Product, two basic product:
* top view counting, simulate by in-out precision
* landscape view counting and recognition, simulate by in-out precision, 
  direction, snapshot ratio, face bucket list.

### stream:
Transfer truth data, prediction data, and some metrics data to database, 
elastic search, and so on. We can have batch stream and real-time stream both.

### tools:
tools module:
* basic: basic tools used by orchestrator.py
* face_recognition: tools used by face bucket or landscape view product

### orchestrator.py
entry of simulator, you can just point out which building info you need to 
use and all the data would be simulated and saved in ./data.

`python3 orchestrator.py --building_name=small-expo --date=2020-07-03`

# Others
### What requests does the arena's connectivity graph design need to fit?
Rangers' activity in arena would be very complex and randomly:
* A: they could just go through the position's passage (usual)
* B: they could choose another way in the same district (likely)
* C: they could make U-turn in front of the position (unlikely)
* D: cashier's position abstract more rangers
* E: they spend variant time in same district
* F: different district's abstraction is also different

Product's also make different data base on ranger's activity and its own 
speciality:
* G: top view and landscape view product could (not always and different 
  possibility for in and out) produce in-out data in A but not for B and C.
* H: landscape view product could (not always and only in one direction) 
  produce face data in A, B and C.

So the connectivity graph design must have enough capacity for handling all 
the situations described above.

Does the conditions' set determine unique design? No, definitely.

There are six mathematically equivalent designs at least.

### Why we have six mathematically equivalent designs at least?
Consider that we have eight conditions listed above, some conditions don't 
make different graph design really. And they are:
* D means we must have weight add-on in our designs.
* E and F means we must have expectation, standard deviation and minimum time 
  cost.
* G and H can be divided to two parts, one is product's own speciality, like
  different possibility and face data availability, the other is related to 
  condition A, B and C

All these three must be existed in graph properties, no matter graph 
properties, vertex properties or edge properties, and they don't make 
remarkable different graph designs.

But condition A, B and C lives really matter!

Condition A, B and C actually means that position, possible path and 
district (atom district) are the most 3 important parts in connectivity graph 
design.

But in graph theory, they only have two first class objects: Vertex and Edge.

It means we have to choose two of 3 important parts as Vertex and Edge, and 
the other have to be properties. so we have C(3, 2) * P(2, 2) = 6 
mathematically equivalent designs, and they are:
* Design A: position as vertex, possible path as edge, district as properties
* Design B: possible path as vertex, position as edge, district as properties
* Design C: position as vertex, district as edge, possible path as properties
* Design D: district as vertex, position as edge, possible path as properties
* Design E: district as vertex, possible path as edge, position as properties
* Design F: possible path as vertex, district as edge, position as properties

### Why I choose Design A for arena's connectivity graph?
Design D and E: district as vertex actually means multiple edges between 
vertex pairs. Many algorithms can not be well defined in this graph and the 
graph would be too complex (Consider that multiple positions in one 
district). And if we can not accept too many trade-off, it cause directed 
graph, also too complex.

Design B and F: possible path as vertex, too abstract to imagine. And it is 
also very hard to predict vertex and generate graph.

Design C: possible path as properties means properties must be iterable and 
the properties' design is too complex.

Only Design A make it simple.
