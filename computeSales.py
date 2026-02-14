# pylint: disable=invalid-name
"""
computeSales.py

Compute total sales cost from product catalogue and sales records.

This program reads a price catalogue and sales records from JSON files,
computes the total cost of all sales, and outputs results to both
the console and a results file.

Usage:
    python computeSales.py priceCatalogue.json salesRecord.json
"""

import json
import sys
import time


def load_json_file(file_path):
    """Load and parse a JSON file, returning the parsed data."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as err:
        print(f"Error: Invalid JSON format in '{file_path}': {err}")
        sys.exit(1)
    return data


def build_price_catalogue(product_list):
    """Build a dictionary mapping product titles to their prices."""
    catalogue = {}
    for item in product_list:
        try:
            title = item.get("title", "")
            price = item.get("price", 0)
            if not title:
                print("Warning: Product entry without title found, skipping.")
                continue
            if not isinstance(price, (int, float)):
                print(f"Warning: Invalid price for '{title}', skipping.")
                continue
            catalogue[title] = float(price)
        except AttributeError:
            print(f"Warning: Invalid product entry: {item}, skipping.")
    return catalogue


def compute_total_sales(catalogue, sales_records):
    """Compute the total cost of all sales based on the price catalogue."""
    total_cost = 0.0
    sale_details = []

    for record in sales_records:
        try:
            product = record.get("Product", "")
            quantity = record.get("Quantity", 0)

            if not product:
                print("Warning: Sale record without product name, skipping.")
                continue

            if not isinstance(quantity, (int, float)) or quantity < 0:
                print(
                    f"Warning: Invalid quantity for '{product}', skipping."
                )
                continue

            if product not in catalogue:
                print(
                    f"Warning: Product '{product}' not found in catalogue, "
                    "skipping."
                )
                continue

            price = catalogue[product]
            subtotal = price * quantity
            total_cost += subtotal
            sale_details.append({
                "product": product,
                "quantity": quantity,
                "price": price,
                "subtotal": subtotal
            })
        except AttributeError:
            print(f"Warning: Invalid sale record: {record}, skipping.")

    return total_cost, sale_details


def format_results(total_cost, sale_details, elapsed_time):
    """Format the sales results into a human-readable string."""
    lines = []
    lines.append("=" * 60)
    lines.append("SALES RESULTS")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"{'Product':<30} {'Qty':>6} {'Price':>10} {'Subtotal':>12}")
    lines.append("-" * 60)

    for detail in sale_details:
        lines.append(
            f"{detail['product']:<30} "
            f"{detail['quantity']:>6} "
            f"${detail['price']:>9.2f} "
            f"${detail['subtotal']:>11.2f}"
        )

    lines.append("-" * 60)
    lines.append(f"{'TOTAL':>48} ${total_cost:>11.2f}")
    lines.append("")
    lines.append(f"Time elapsed: {elapsed_time:.4f} seconds")
    lines.append("=" * 60)

    return "\n".join(lines)


def save_results(results_text, output_file="SalesResults.txt"):
    """Save the results to a text file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(results_text)
        print(f"\nResults saved to '{output_file}'")
    except IOError as err:
        print(f"Error: Could not write to '{output_file}': {err}")


def main():
    """Main function to orchestrate the sales computation."""
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json "
              "salesRecord.json")
        sys.exit(1)

    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    start_time = time.time()

    product_list = load_json_file(catalogue_file)
    sales_records = load_json_file(sales_file)

    catalogue = build_price_catalogue(product_list)
    total_cost, sale_details = compute_total_sales(catalogue, sales_records)

    elapsed_time = time.time() - start_time

    results_text = format_results(total_cost, sale_details, elapsed_time)
    print(results_text)
    save_results(results_text)


if __name__ == "__main__":
    main()
