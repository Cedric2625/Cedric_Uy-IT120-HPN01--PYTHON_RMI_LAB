# server.py - same as ProductImpl.java, ServerImpl.java and Server.java
import threading
import Pyro5.api
import Pyro5.nameserver
from product import Product


def log(msg):
    print(f"[SERVER] {msg}", flush=True)


# ProductImpl.java - the real product object, lives on the server
@Pyro5.api.expose
class ProductImpl(Product):
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    def get_name(self):
        log(f"get_name() called on '{self.name}'")
        return self.name

    def get_price(self):
        log(f"get_price() called on '{self.name}'")
        return self.price

    def get_description(self):
        log(f"get_description() called on '{self.name}'")
        return self.description


# ServerImpl.java - the remote store that gives products to clients
@Pyro5.api.expose
class ServerImpl:
    def __init__(self, products):
        self.products = products

    def list_products(self):
        log("Client asked for the product list")
        return list(self.products)

    def get_product(self, code):
        log(f"Client asked for product '{code}'")
        if code not in self.products:
            raise ValueError(f"No product with code '{code}'")
        return self.products[code]  # sent as a remote reference (stub), not a copy


# Server.java - starts everything
def main():
    print("=" * 50)
    print("   PYTHON RMI SERVER (Pyro5) - Product Store")
    print("=" * 50)

    # Start the name server (like rmiregistry)
    _, ns_daemon, _ = Pyro5.nameserver.start_ns(host="localhost", port=9090)
    threading.Thread(target=ns_daemon.requestLoop, daemon=True).start()

    products = {
        "laptop": ProductImpl("Laptop", 45999.00, "A 15-inch laptop for school and work."),
        "phone": ProductImpl("Smartphone", 15999.00, "A fast phone with a great camera."),
        "toaster": ProductImpl("Toaster", 1299.50, "Makes crispy toast in 2 minutes."),
    }

    # Register the objects so clients can call them
    daemon = Pyro5.api.Daemon(host="localhost")
    for p in products.values():
        daemon.register(p)
    uri = daemon.register(ServerImpl(products))

    # Bind the store to a name (like Naming.rebind)
    Pyro5.api.locate_ns(host="localhost", port=9090).register("store.server", uri)

    log("Server is ready. Waiting for clients... (Ctrl+C to stop)")
    print("-" * 50)
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        log("Shutting down...")


if __name__ == "__main__":
    main()
