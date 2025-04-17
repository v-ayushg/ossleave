import csv

def export_csv(data):
    filepath = 'leave_records.csv'
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Leave Dates'])
        for entry in data:
            writer.writerow([entry['name'], ', '.join(entry['dates'])])
    return filepath
