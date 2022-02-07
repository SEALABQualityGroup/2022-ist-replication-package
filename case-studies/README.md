## Train Ticket Booking Service (TTBS)

Train Ticket Booking Service (TTBS) is a web-based booking application, and its architecture is based on the microservice paradigm. The system is made up of 40 microservices, and it provides different scenarios through users that can perform realistic operations, e.g., book a ticket or watch trip information like intermediate stops. The application employs a docker container for each microservice, and connections among them are managed by a central pivot container.

Our UML model of TTBS is available online.
The static view is made of **11 UML Component**, where each component represents a microservice. In the deployment view, instead, we consider **11 UML Nodes**, each one representing a docker container.

Among all available TTBS scenarios shown in~\cite{DBLP:conf/staf/Pompeo0CE19}, we have considered **3 UML UseCases**, namely *login*, *update user details* and *rebook*. We selected these three scenarios because they commonly represent performance-critical ones in a ticketing booking service. In particular,  each scenario is described by a UML Sequence Diagram. Furthermore, the model comprises two user categories: simple and admin users. The simple user category can perform the login and the rebook scenarios, while the admin category can perform the login and the update user details scenarios.

## CoCoMe

The component-based system engineering domain has always been characterized by a plethora of standards for implementing, documenting, and deploying components.  These standards are well-known as component models. Before the birth of the common component modeling example (CoCoME) \cite{Herold2008}, it was hard for researchers to compare different component models. CoCoME is a case study that acts as a single specification to be implemented using different component models.

CoCoME describes a Trading System containing several stores. A store might have one or more cash desks for processing goodies. A cash desk is equipped with all the tools needed to serve a customer (e.g., a Cash Box, Printer, Bar Code Scanner). CoCoME covers possible scenarios performed at a cash desk. For example, scanning products, paying by credit card, generating reports, or ordering new goodies. A set of cash desks forms a cash desk line. The latter is connected to the store server for registering cash desk line activities. Instead, a set of stores is organized in an enterprise having its server for monitoring stores operations. 

CoCoME describes 8 scenarios involving more than 20 components. We implemented the case study using UML and, for our analysis, we downsized CoCoME selecting **3 UML UseCases**, **13 UML Components**, and **8 UML Nodes**. We selected three scenarios from CoCoME: UC1, UC4 and UC5. UC1 describes the arrival of a customer at the checkout, identification, and sale of a product. UC4 represents how products are registered in the store database upon their arrival. Instead, the UC5 represents the possibility of generating a report of store activities.
