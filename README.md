# Python RMI Lab (Pyro5)

A Python version of the Java RMI project `JAVA_RMI_IV`, built with **Pyro5** (Python Remote Objects).

## How the files match

| Java file (JAVA_RMI_IV) | Python file | What it does |
|---|---|---|
| `Product.java` | `product.py` | Remote interface: the list of methods a product must have |
| `ProductImpl.java` | `server.py` → `class ProductImpl` | The real product object that runs on the server |
| `ServerImpl.java` | `server.py` → `class ServerImpl` | The remote store that gives products to clients |
| `Server.java` | `server.py` → `main()` | Starts the registry, registers the objects, waits for clients |
| `Client.java` | `client.py` | Finds the store, gets products, calls their methods |

## Java RMI vs Pyro5

| Java RMI | Pyro5 |
|---|---|
| `interface Product extends Remote` | `class Product(ABC)` with `@abstractmethod` |
| `extends UnicastRemoteObject` | `@Pyro5.api.expose` + `daemon.register(obj)` |
| `rmiregistry` / `LocateRegistry.createRegistry()` | Pyro5 Name Server (`start_ns`) |
| `Naming.rebind("name", obj)` | `ns.register("name", uri)` |
| `Naming.lookup("rmi://...")` | `Pyro5.api.Proxy("PYRONAME:...")` |
| Stub | Proxy |
| `RemoteException` | `Pyro5.errors.CommunicationError` |

## How to run

1. Install Pyro5:
   ```
   pip install Pyro5
   ```
2. **Terminal 1**: start the server. It also starts the name server, so there is no separate `rmiregistry` step.
   ```
   python server.py
   ```
3. **Terminal 2**: run the client:
   ```
   python client.py
   ```

## Expected output

**Server (Terminal 1)**
```
==================================================
   PYTHON RMI SERVER (Pyro5) - Product Store
==================================================
[SERVER] Server is ready. Waiting for clients... (Ctrl+C to stop)
--------------------------------------------------
[SERVER] Client asked for the product list
[SERVER] Client asked for product 'laptop'
[SERVER] get_name() called on 'Laptop'
[SERVER] get_price() called on 'Laptop'
[SERVER] get_description() called on 'Laptop'
...
[SERVER] Client asked for product 'tablet'
```

**Client (Terminal 2)**
```
==================================================
   PYTHON RMI CLIENT (Pyro5) - Product Store
==================================================
Products on the server: ['laptop', 'phone', 'toaster']
--------------------------------------------------
  Name        : Laptop
  Price       : PHP 45,999.00
  Description : A 15-inch laptop for school and work.
--------------------------------------------------
  Name        : Smartphone
  Price       : PHP 15,999.00
  Description : A fast phone with a great camera.
--------------------------------------------------
  Name        : Toaster
  Price       : PHP 1,299.50
  Description : Makes crispy toast in 2 minutes.
--------------------------------------------------
Asked for 'tablet' -> Server error: No product with code 'tablet'
```

The server prints a `[SERVER]` line for every call the client makes. That shows the methods run on the server, not on the client, which is the main idea of RMI.
