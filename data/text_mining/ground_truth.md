# Ground Truth Dataset for Ownership Extraction Validation

This file contains manually verified ownership data for testing the extractor's accuracy.

---

## Sample 1: RHB Bank Berhad (sample_complex_malaysian_company.txt)

### Ground Truth: Top 10 Shareholders

| Rank | Shareholder | Percentage | Type | Foreign | Government |
|------|-------------|------------|------|---------|-----------|
| 1 | Employees Provident Fund (EPF) | 35.25% | Direct/Beneficial | No | Yes |
| 2 | Kumpulan Wang Simpanan Pekerja (KWAP) | 12.50% | Direct | No | Yes |
| 3 | Khazanah Nasional Berhad | 10.00% | Direct | No | Yes |
| 4 | Kuwait Finance House (Malaysia) Berhad | 8.75% | Direct | No | No |
| 5 | Singapore Holdings Pte Ltd | 6.25% | Direct | Yes | No |
| 6 | Global Investment Management Inc | 5.50% | Direct | Yes | No |
| 7 | Permodalan Nasional Berhad (PNB) | 4.80% | Direct | No | Yes |
| 8 | Lembaga Tabung Haji | 3.20% | Direct | No | Yes |
| 9 | Amanah Saham Nasional Berhad | 2.15% | Direct | No | Yes |
| 10 | Rizal Merchant Bankers Berhad | 1.80% | Direct | No | No |

### Expected Metrics:
- Total shareholders: 10
- Total ownership: 90.20%
- Foreign owners: 2
- Government owners: 6
- Control relationships (10%+): 3

---

## Sample 2: Celcom Digital Berhad (sample_telecom_company.txt)

### Ground Truth: Top 10 Shareholders

| Rank | Shareholder | Percentage | Type | Foreign | Government |
|------|-------------|------------|------|---------|-----------|
| 1 | Axiata Group Berhad | 48.90% | Direct | No | No |
| 2 | Telekom Malaysia Berhad | 32.10% | Direct | No | Yes |
| 3 | Kumpulan Wang Persaraan (KWAP) | 8.50% | Direct | No | Yes |
| 4 | Employees Provident Fund (EPF) | 6.25% | Direct | No | Yes |
| 5 | Permodalan Nasional Berhad | 1.85% | Direct | No | Yes |
| 6 | Lembaga Tabung Haji | 1.20% | Direct | No | Yes |
| 7 | Amanah Saham Nasional Berhad | 0.85% | Direct | No | Yes |
| 8 | CIMB Bank Berhad | 0.45% | Direct | No | No |
| 9 | Maybank Investment Bank Berhad | 0.32% | Direct | No | No |
| 10 | RHB Bank Berhad | 0.28% | Direct | No | No |

### Expected Metrics:
- Total shareholders: 10
- Total ownership: 100.72% (includes joint venture interests)
- Foreign owners: 0
- Government owners: 5
- Control relationships (10%+): 2

### Note:
- Joint ventures (Celcom Axiata Berhad 60%, etc.) are NOT shareholders but company investments
- Total > 100% due to joint venture interests listed alongside shareholders

---

## Sample 3: Petronas Gas Berhad (sample_energy_company.txt)

### Ground Truth: Top 10 Shareholders

| Rank | Shareholder | Percentage | Type | Foreign | Government |
|------|-------------|------------|------|---------|-----------|
| 1 | PETRONAS Capital Bhd | 50.00% | Direct | No | Yes (GLC) |
| 2 | Khazanah Nasional Berhad | 15.00% | Direct | No | Yes |
| 3 | Employees Provident Fund | 10.00% | Direct | No | Yes |
| 4 | Kumpulan Wang Simpanan Pekerja | 5.00% | Direct | No | Yes |
| 5 | Permodalan Nasional Berhad | 3.00% | Direct | No | Yes |
| 6 | Amanah Saham Nasional Berhad | 2.00% | Direct | No | Yes |
| 7 | Lembaga Tabung Haji | 1.50% | Direct | No | Yes |
| 8 | State of Johor Investment Corporation | 1.00% | Direct | No | Yes |
| 9 | Singapore Power Ltd | 0.50% | Direct | Yes | No |
| 10 | Abu Dhabi National Energy Company | 0.40% | Direct | Yes | No |

### Expected Metrics:
- Total shareholders: 10
- Total ownership: 88.40%
- Foreign owners: 2
- Government owners: 8
- Control relationships (10%+): 3

### Note:
- Petroliam Nasional Berhad (Petronas) at 0.25% is INDIRECT ownership
- Total > 100% includes cross-holding mentions

---

## Sample 4: Malaysia Airports Holdings Berhad (sample_narrative_company.txt)

### Ground Truth: Top 10 Shareholders

| Rank | Shareholder | Percentage | Type | Foreign | Government |
|------|-------------|------------|------|---------|-----------|
| 1 | Ministry of Finance Malaysia | 53.45% | Direct | No | Yes |
| 2 | Khazanah Nasional Berhad | 25.80% | Direct | No | Yes |
| 3 | Employees Provident Fund | 12.30% | Direct | No | Yes |
| 4 | Kumpulan Wang Simpanan Pekerja | 5.20% | Direct | No | Yes |
| 5 | Permodalan Nasional Berhad | 1.85% | Direct | No | Yes |
| 6 | Lembaga Tabung Haji | 1.20% | Direct | No | Yes |
| 7 | Singapore Changi Airport Fund | 0.15% | Direct | Yes | No |
| 8 | Dubai Airports Investment LLC | 0.05% | Direct | Yes | No |

### Expected Metrics:
- Total shareholders: 8
- Total ownership: 100.00%
- Foreign owners: 2
- Government owners: 6
- Control relationships (10%+): 3

### Note:
- Narrative format with embedded percentages
- Ownership structure described in paragraphs

---

## Validation Metrics

### Precision
- **Definition:** TP / (TP + FP)
- **Meaning:** Of all extracted shareholders, how many are correct?

### Recall
- **Definition:** TP / (TP + FN)
- **Meaning:** Of all actual shareholders, how many were extracted?

### F1 Score
- **Definition:** 2 * (Precision * Recall) / (Precision + Recall)
- **Meaning:** Harmonic mean of precision and recall

### Accuracy
- **Definition:** (TP + TN) / (TP + TN + FP + FN)
- **Meaning:** Overall correctness of extraction

---

## Evaluation Criteria

### Excellent Performance
- Precision: > 90%
- Recall: > 90%
- F1 Score: > 90%

### Good Performance
- Precision: 75-90%
- Recall: 75-90%
- F1 Score: 75-90%

### Acceptable Performance
- Precision: 60-75%
- Recall: 60-75%
- F1 Score: 60-75%

### Needs Improvement
- Precision: < 60%
- Recall: < 60%
- F1 Score: < 60%

---

## Use This Ground Truth

Run the validation script to compare extractor output against this ground truth and calculate metrics.

**Command:**
```bash
python3 validate_extractor.py
```

**Output:**
- Precision, Recall, F1 Score for each sample
- Overall metrics across all samples
- Error analysis (false positives, false negatives)
