# Text Mining for BPM7 External Sector Statistics

## Overview

This module implements text mining techniques to extract ownership information from Malaysian corporate documents, supporting BPM7 external sector statistics compilation.

## Components

### 1. Ownership Extraction

**File:** `ownership_extractor_v2.py`

**Purpose:** Extracts ownership relationships from structured text formats in annual reports.

**Capabilities:**
- ✅ Extract shareholder names and percentages from list formats
- ✅ Identify control relationships (10%+ threshold per BPM7)
- ✅ Classify ownership type (direct, indirect, beneficial)
- ✅ Identify foreign vs. domestic entities
- ✅ Identify government/sovereign entities
- ✅ Calculate completeness metrics
- ✅ Prioritize Direct Investment candidates

**Input formats supported:**
```
1. Company Name - XX.XX%
2. Another Company Ltd - YY.Y%
```

**Output:**
- Structured ownership relationships with metadata
- Completeness analysis
- DI candidate prioritization

### 2. Usage Example

```python
from src.text_mining.ownership_extractor_v2 import OwnershipExtractorV2

# Initialize extractor
extractor = OwnershipExtractorV2()

# Load document text
with open('annual_report.txt', 'r') as f:
    text = f.read()

# Extract ownership relationships
relationships = extractor.extract_ownership_from_list(text, "ABC Berhad")

# Filter control relationships (10%+)
control_rels = extractor.filter_control_relationships(relationships)

# Identify DI candidates
di_candidates = extractor.extract_direct_investment_candidates(relationships)

# Analyze completeness
analysis = extractor.analyze_completeness(relationships)
```

## BPM7 Applications

### 1. Control Relationship Detection
- Identifies entities with 10%+ ownership (BPM7 control threshold)
- Distinguishes direct vs. indirect ownership
- Classifies as DI vs. PI based on control

### 2. Direction of Investment
- Foreign entities → Inward DI
- Domestic entities with foreign parents → Outward DI
- Ultimate beneficial owner tracing

### 3. Coverage Assessment
- Compares extracted ownership with survey frames
- Identifies missing entities
- Prioritizes data collection

## Current Status

✅ **Implemented:**
- Regex-based ownership extraction from list formats
- Control threshold filtering (10%+)
- Foreign/government entity identification
- Completeness analysis
- DI candidate scoring

⏸️ **Next Steps:**
- Table format extraction
- PDF parsing for annual reports
- Named Entity Recognition (NER) for unstructured text
- Relationship inference from partial data
- Validation against ground truth

## Testing

Run the test suite:
```bash
python src/text_mining/ownership_extractor_v2.py
```

Expected output:
- Extracted ownership relationships
- Completeness metrics
- Control relationships (10%+)
- DI candidate prioritization

## Limitations

1. **Structured formats only** - Currently handles list formats, not free text
2. **Heuristic-based** - Foreign/government detection uses simple pattern matching
3. **No document parsing** - Requires pre-extracted text (not PDF-ready)
4. **No validation** - No ground truth comparison yet

## Data Sources

### Target Sources (Malaysia)
- Bursa Malaysia annual reports
- SSM (Suruhanjaya Syarikat Malaysia) filings
- Corporate announcements
- Shareholder circulars

### Access Methods
- Bursa Marketplace (public)
- Company websites (public)
- SSM e-Info (subscription)

## Performance Metrics

To be validated:
- Precision: % of extracted relationships that are correct
- Recall: % of actual relationships that are extracted
- F1-score: Harmonic mean of precision and recall

## Integration with Existing Framework

The text mining module complements the existing GLEIF-based entity discovery:

```
GLEIF Data          Text Mining
    ↓                    ↓
Entity Catalog    →  Ownership Graph
    ↓                    ↓
Coverage Gap      →  Relationship Extraction
```

**Combined value:**
1. GLEIF provides entity catalog (who exists)
2. Text mining provides ownership (who owns whom)
3. Combined → Complete external sector picture

## Future Enhancements

### Phase 2 (6 months)
- PDF document parsing
- Named Entity Recognition (NER)
- Improved context understanding
- Entity resolution across documents

### Phase 3 (12 months)
- Graph Neural Networks for link prediction
- Ultimate beneficial owner tracing
- Intermediate jurisdiction detection
- Real-time monitoring of ownership changes

## References

- BPM7 Manual (IMF)
- Malaysian Companies Act 2016
- Bursa Malaysia Listing Requirements
- GLEIF API Documentation
