"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """
    marketplace = None
    wait_time = 0.0

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor which is used to add a producer to the Marketplace.
        """
        super().__init__(**kwargs)
        self.products = products
        self.marketplace = marketplace
        self.wait_time = republish_wait_time
        self.prod_id = self.marketplace.register_producer()

    def run(self):
        """
        The thread function of the producer continuously iterates through the product 
        list and attempts to publish each product until all products of that type are 
        successfully published. If a product is published, the producer then waits for 
        the amount of time specified for that product before moving on to the next one. 
        If a publish operation fails, the producer waits for a set amount of time before 
        trying again. This process repeats indefinitely until the program is terminated.
        """

        while True:

            while True:
                # Iterate over the list of products to produce
                for i, product in enumerate(self.products):
                    # retrieves the values product, num_prod, and wait_time at the index
                    # i using indexing
                    product = self.products[i][0]
                    num_prod = self.products[i][1]
                    wait_time = self.products[i][2]
                    # Produce the specified number of products
                    for _ in range(num_prod):
                        # Try to publish the product and check for any errors
                        while not self.marketplace.publish(str(self.prod_id), product):
                            # If the operation fails and the producer didnt publicate a product,
                            # wait for a specified wait_time before to try again.
                            sleep(self.wait_time)
                        # if it is done succesfully, wait for the specified time before moving
                        # on to the next product.
                        sleep(wait_time)
