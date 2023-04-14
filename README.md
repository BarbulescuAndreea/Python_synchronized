## `assignments/`

Contains skeletons and tests.

The implementated solution is based on a marketplace that serves as a central hub
for producers an consumers. The marketplace acts as a buffer between the producers and consumers, ensuring that products are delivered to the right clients. The implementation is based on a threaded approach, where each producer and consumer run its own thread.

The 'Marketplace' class is responsible for keeping track of the available
products. I used synchronization methods such as Lock() and Semaphore() to ensure that the shared data(ex: the published products/the registered consumers and producers) are accessed and modified in a thread-safe manner. In particular, I used a 'Lock' object to protect the 'products' dictionary from simultaneous modification by multiple threads. I also used Semaphores to control access to the list of products that were available for sale. My Semaphores act as a mutex in the code, having an initial value of 1.

The 'Producer' class represents a producer in the system, which can produce and
publish products to the marketplace. The run method of this class continuously iterates throuhgh the list of products th produce and attempts to publish each product untill all products of that type are succesfully published. If product is published, the producer then waits for the amount of time specified for that product before moving on to the next one. This process repeats indefinetely until the program is terminated.

The 'Consumer' class represents a producer in the system, which can purchase
products from the marketplace. The run method of this class iterates through the list of products to purchase and attempts to purchase each product untill all products of that type are succesfully purchased. This process also repeats indefinetely until the program is terminated.

I implemented the -unittests- in order to test each function from the
Marketplace class. The tests were organized into separate test cases, each testing a specific aspect which I could think about of its corresponding function. This tests helped me to better understand their importance and ensure the quality and stability of the code.

I implemented the -loggin- system which I found important because it showed me the
informations about the execution of the program. But that didn t work when i submitted to the vmchecker so i deleted it.

The implemented solution is useful for scenarios where there is a need for
centralized hub to manage the exchange of products between producers and consumers. I consider this homework usefull because it helped me to gain a deeper understanding of concurrent programming concepts and techniques, and i had the oportunity to practice implementing these concepts in Python.

The implementation can be furthed improved by adding more errors handling and
better synchronization mechanisms between threads.

I had some difficulties such as synchronization issues, more clearly when multiple
threads tried to access and modify the same shared data structures, or deadlock when threads were waiting for each other to release a resource, or with the unitttesting because I wasn't sure at the very begining how this works, but I managed to solve them succesfully.

I don t have any extra functionalities. On my laptop, all 
the 10 tests pass succesfully and i have 9.75/10 with pylint.
