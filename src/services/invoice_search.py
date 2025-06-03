from helper import load_json
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
INVOICE_JSON = load_json(project_root, "invoices")

def search_invoices(query):
    query = query.lower()
    results = []

    for invoice in INVOICE_JSON:
        match = False
        for key, value in invoice.items():
            if value is not None and str(value).lower().find(query) != -1:
                match = True
                break
        if match:
            results.append(invoice)

    return results

if __name__ == "__main__":
    query = "Aaron"
    matches = search_invoices(query)

    print(f"\nFound {len(matches)} matching invoices(s):")
    for idx, invoice in enumerate(matches, start=1):
        print(f"{idx}. Invoice #: {invoice.get('Invoice Number', 'N/A')} | Bill To: {invoice.get('Bill To', 'N/A')} | Item: {invoice.get('Item', 'N/A')}")
