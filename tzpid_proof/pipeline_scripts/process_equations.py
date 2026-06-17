import csv
import os
import re

input_file = r'd:\tzpidNEW\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv'
temp_file = r'd:\tzpidNEW\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export_temp.csv'

def extract_symbols(eq):
    parts = re.split(r'[\s=\+\-\*/\(\)\,\;\|]+', str(eq))
    symbols = [p for p in parts if len(p.strip()) > 0 and p.strip() not in ['in', 'to', 'text', 'and', 'for', 'is', 'not', 'exist', 'does']]
    return list(dict.fromkeys(symbols))[:3]

def generate_progression(statement, equation):
    eq = str(equation).strip()
    symbols = extract_symbols(eq)
    sym_text = ", ".join([f"{s}" for s in symbols]) if symbols else "the key variables"
    
    step1 = f"Identify the core components and domain from the premise (e.g., {sym_text})."
    
    if "||" in eq:
        step2 = "Establish the multi-condition or piecewise mathematical relationships required by the system."
    elif "\\lim" in eq or "\\int" in eq or "\\oint" in eq or "\\nabla" in eq:
        step2 = "Apply calculus operations or boundary limits to constrain the identified variables."
    elif "\\forall" in eq or "\\exists" in eq or "\\in" in eq:
        step2 = "Formulate the logical conditions and quantifiers as dictated by the manifold properties."
    elif "text" in eq or "det" in eq or "dim" in eq:
        step2 = "Define the structural or geometric constraints (such as dimensionality or metric properties)."
    else:
        step2 = "Formulate the foundational algebraic relationship between the components."
        
    step3 = f"Formalize the complete mathematical expression, yielding the final canonical form: {eq}"
    
    return step1, step2, step3

def process_csv():
    # Check if we need to resume
    processed_count = 0
    
    # Read all rows into memory to modify them, or do it streaming
    # We will do it streaming.
    
    rows = []
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        # Check if columns exist
        col1, col2, col3 = "equation support 1", "equation support 2", "equation support 3"
        if col1 not in headers:
            headers.extend([col1, col2, col3])
            
        col1_idx = headers.index(col1)
        col2_idx = headers.index(col2)
        col3_idx = headers.index(col3)
        
        stat_idx = headers.index("canonical_statement")
        eq_idx = headers.index("canonical_equation")
        
        for row in reader:
            # Pad row if needed
            while len(row) < len(headers):
                row.append("")
            rows.append(row)

    print(f"Total rows to process: {len(rows)}")

    # Process and save in chunks of 100
    chunk_size = 100
    updates_in_current_chunk = 0
    total_updates = 0
    
    # Open temp file for writing incrementally
    with open(temp_file, 'w', encoding='utf-8-sig', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(headers)
        
        for i, row in enumerate(rows):
            # Check if it needs processing
            if not row[col1_idx] or not row[col2_idx] or not row[col3_idx]:
                statement = row[stat_idx]
                equation = row[eq_idx]
                s1, s2, s3 = generate_progression(statement, equation)
                row[col1_idx] = s1
                row[col2_idx] = s2
                row[col3_idx] = s3
                updates_in_current_chunk += 1
                total_updates += 1
            
            writer.writerow(row)
            
            # Save after every 100 updates
            if updates_in_current_chunk >= chunk_size:
                f_out.flush()
                os.fsync(f_out.fileno())
                updates_in_current_chunk = 0
                print(f"Processed and saved {i+1} rows (Total updates: {total_updates})...")
                
    # Replace original file with the updated one
    os.replace(temp_file, input_file)
    print(f"Finished! Total new equations processed: {total_updates}")

if __name__ == "__main__":
    process_csv()
