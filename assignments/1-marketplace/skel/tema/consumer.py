"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread, current_thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """
    marketplace = None
    carts = []
    retry_wait_time = 0.0
    cart_id = -1

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor which is used in order to create a consumer.
        """

        # calling the __init__() method of the parent class Thread with
        # the arguments that can be passed.
        super().__init__(**kwargs)
        self.carts = carts
        self.marketplace = marketplace # refer the marketplace.
        self.retry_wait_time = retry_wait_time

    def set_cart_id(self):
        """
        Simply return the cart_id
        """
        self.cart_id = self.marketplace.new_cart()

    def possible_operations(self):
        """
        # the operations that a consumer/client can perform are: remove/add an item from the cart.
        """
        self.operations = {}
        self.operations["remove"] = self.marketplace.remove_from_cart
        self.operations["add"] = self.marketplace.add_to_cart

    def run(self):
        """
            The first thing that a consumer must have in order to perform operations over 
        a cart is the cart_id. The code iterates over a list of carts, and for each cart 
        it creates a new cart in the marketplace, and perform the operations on it (add/remove), 
        then places an order for the cart. If the operation fails, waits for a specified time.
        """

        for current_cart in self.carts:

            self.set_cart_id()
            cart = {"operations" : current_cart} # dictionary key-value, where the key is the
                                # operations and the value is the current cart being processed

            self.possible_operations()
            cart_operations = cart.get("operations", []) # retrieves the value of the
                                        # "operations" key from the cart dictionary.
            for current_operation in cart_operations:
                # nr_ops_existent keep the numbers of the current operations
                # that needs to be performed.
                nr_ops_existent = current_operation.get("quantity", 0)
                for _ in range(nr_ops_existent):
                    # extract the type of operation - add/remove
                    operation_type = current_operation.get("type", "")
                    # extract the product on which the consumer needs to perform the operation.
                    product = current_operation.get("product", "")
                    success = False
                    while not success:
                        # performeaza actiunea asupra produsului din cosul corespunzator(cart_id).
                        exit_code = self.operations.get(operation_type, None)(self.cart_id, product)
                        # If ret is False, the consumer waits for a certain amount of time
                        # (as specified by self.retry_wait_time) before retrying the operation.
                        if exit_code is None or exit_code is True:
                            success = True
                        else:
                            sleep(self.retry_wait_time)
            # prints out the thread name and item name for each item in the list
            purchased_items = self.marketplace.place_order(self.cart_id)
            for item in purchased_items:
                # used f-string to insert the variable "item" inside the string directly
                print(f"{current_thread().name} bought {item}", flush=True)
                