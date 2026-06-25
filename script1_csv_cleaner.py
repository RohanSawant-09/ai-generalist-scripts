import csv

# Load the CSV file
def load_csv(filepath):
    rows = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows

data = load_csv('customers.csv')
print(f"Loaded {len(data)} rows")
print(data[0])

def is_valid_email(email):
    return '@' in email and '.' in email.split('@')[-1]

def clean_row(row):
    cleaned= {}
    cleaned['name'] = row['name'].strip()
    cleaned['email'] = row['email'].strip()
    cleaned['company'] = row['company'].strip()
    cleaned['status'] = row['status'].strip()
    return cleaned

def process_data(rows):
    clean_data = []
    rejected_data = []

    for row in rows:
        cleaned = clean_row(row)

        if not cleaned['email']:
            cleaned['issue']='missing mail'
            rejected_data.append(cleaned)
        
        elif not is_valid_email(cleaned['email']):
            cleaned['issue']= 'invalid email'
            rejected_data.append(cleaned)

        else:
            clean_data.append(cleaned)
    
    return clean_data, rejected_data

def save_csv(rows, filepath):
    if not rows:
        print(f"No data to save to {filepath}")
        return
    
    fieldnames = rows[0].keys()

    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Saved {len(rows)} rows to {filepath}")

# Run the full pipeline
clean, rejected = process_data(data)

# Save outputs
save_csv(clean, 'customers_clean.csv')
save_csv(rejected, 'customers_rejected.csv')

# Final summary
print(f"\n--- Pipeline Complete ---")
print(f"Total rows processed: {len(data)}")
print(f"Clean rows saved: {len(clean)}")
print(f"Rejected rows saved: {len(rejected)}")