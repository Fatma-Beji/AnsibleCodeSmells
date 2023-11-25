import pandas as pd

# Initialize counters
total_cells = 0
full_agreements = 0
partial_agreements = 0

# Read Excel file
df = pd.read_excel('Annotation.xlsx')  # Replace 'your_file.xlsx' with your actual file name

# Loop through rows and columns
for index, row in df.iterrows():
    row_contains_single_F_or_N = False
    for cell in row:
        total_cells += 1  # Increment the total cell count
        if pd.isna(cell):
            full_agreements += 1
        elif cell == '#':
            full_agreements += 1
        elif 'F' in cell and 'N' in cell:
            partial_agreements += 0.5  # You can choose how much a partial agreement is worth
        else:
            full_agreements += 1
            
        if cell == 'F' or cell == 'N':
            row_contains_single_F_or_N = True
    
    #if row_contains_single_F_or_N:
        #print(f"Row {index + 1} contains a cell with only 'F' or 'N': {row.to_list()}")

# Calculate the agreement score
total_agreement = full_agreements + partial_agreements

if total_cells == 0:
    print("No cells found for comparison.")
else:
    percentage_agreement = (total_agreement / total_cells) * 100
    print(f"Percentage Agreement: {percentage_agreement}%")
