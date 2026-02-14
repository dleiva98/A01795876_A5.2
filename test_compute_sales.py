"""Unit tests for computeSales.py"""

import unittest
import os
import subprocess
import json


class TestComputeSalesTC1(unittest.TestCase):
    """Test Case 1: Basic sales computation with valid data."""

    def test_tc1_execution(self):
        """TC1: Program executes without errors."""
        result = subprocess.run(
            ["python", "computeSales.py",
             "TC1/TC1.ProductList.json", "TC1/TC1.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        self.assertEqual(result.returncode, 0)

    def test_tc1_total(self):
        """TC1: Total cost is correctly computed."""
        result = subprocess.run(
            ["python", "computeSales.py",
             "TC1/TC1.ProductList.json", "TC1/TC1.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        self.assertIn("2945.40", result.stdout)

    def test_tc1_results_file(self):
        """TC1: Results file is created."""
        subprocess.run(
            ["python", "computeSales.py",
             "TC1/TC1.ProductList.json", "TC1/TC1.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        self.assertTrue(os.path.exists("SalesResults.txt"))

    def test_tc1_time_elapsed(self):
        """TC1: Time elapsed is shown in output."""
        result = subprocess.run(
            ["python", "computeSales.py",
             "TC1/TC1.ProductList.json", "TC1/TC1.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        self.assertIn("Time elapsed:", result.stdout)


class TestComputeSalesTC2(unittest.TestCase):
    """Test Case 2: Larger dataset with 10 products."""

    def test_tc2_execution(self):
        """TC2: Program handles larger dataset."""
        result = subprocess.run(
            ["python", "computeSales.py",
             "TC2/TC2.ProductList.json", "TC2/TC2.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        self.assertEqual(result.returncode, 0)

    def test_tc2_total(self):
        """TC2: Total cost is correctly computed for larger dataset."""
        result = subprocess.run(
            ["python", "computeSales.py",
             "TC2/TC2.ProductList.json", "TC2/TC2.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        self.assertIn("10264.08", result.stdout)

    def test_tc2_all_products_listed(self):
        """TC2: All products appear in the output."""
        result = subprocess.run(
            ["python", "computeSales.py",
             "TC2/TC2.ProductList.json", "TC2/TC2.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        with open("TC2/TC2.ProductList.json", 'r',
                  encoding='utf-8') as prod_file:
            products = json.load(prod_file)
        for product in products:
            self.assertIn(product["title"], result.stdout)


class TestComputeSalesTC3(unittest.TestCase):
    """Test Case 3: Invalid data handling."""

    def test_tc3_handles_invalid_data(self):
        """TC3: Program handles invalid data without crashing."""
        result = subprocess.run(
            ["python", "computeSales.py",
             "TC3/TC3.ProductList.json", "TC3/TC3.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        self.assertEqual(result.returncode, 0)

    def test_tc3_warnings_displayed(self):
        """TC3: Warnings are shown for invalid entries."""
        result = subprocess.run(
            ["python", "computeSales.py",
             "TC3/TC3.ProductList.json", "TC3/TC3.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        output = result.stdout + result.stderr
        self.assertIn("Warning", output)

    def test_tc3_total_excludes_invalid(self):
        """TC3: Total only includes valid sales."""
        result = subprocess.run(
            ["python", "computeSales.py",
             "TC3/TC3.ProductList.json", "TC3/TC3.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        self.assertIn("4011.73", result.stdout)

    def test_tc3_missing_file(self):
        """TC3: Program handles missing file gracefully."""
        result = subprocess.run(
            ["python", "computeSales.py",
             "nonexistent.json", "TC3/TC3.Sales.json"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        self.assertNotEqual(result.returncode, 0)

    def test_tc3_wrong_arguments(self):
        """TC3: Program shows usage when wrong number of args."""
        result = subprocess.run(
            ["python", "computeSales.py"],
            capture_output=True, text=True, timeout=30,
            check=False
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout)


if __name__ == "__main__":
    unittest.main()
