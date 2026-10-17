# client.py - same as Client.java
import Pyro5.api
import Pyro5.errors


def main():
    print("=" * 50)
    print("   PYTHON RMI CLIENT (Pyro5) - Product Store")
    print("=" * 50)

    try:
        # Look up the store by name (like Naming.lookup)
        with Pyro5.api.Proxy("PYRONAME:store.server@localhost:9090") as store:
            codes = store.list_products()
            print(f"Products on the server: {codes}")
            print("-" * 50)

            # Each method call below runs on the server
            for code in codes:
                product = store.get_product(code)
                print(f"  Name        : {product.get_name()}")
                print(f"  Price       : PHP {product.get_price():,.2f}")
                print(f"  Description : {product.get_description()}")
                print("-" * 50)

            # Ask for a product that does not exist
            try:
                store.get_product("tablet")
            except ValueError as e:
                print(f"Asked for 'tablet' -> Server error: {e}")

    except (Pyro5.errors.CommunicationError, Pyro5.errors.NamingError):
        print("ERROR: Cannot reach the server. Run 'python server.py' first.")


if __name__ == "__main__":
    main()
