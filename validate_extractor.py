"""
Ownership Extractor Validation Script

Compares extractor output against ground truth and calculates metrics.
"""

import re
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Import the extractor
import sys
sys.path.insert(0, '/data/Projects/bpm2007_ml_explorer-experiment')
from src.text_mining.ownership_extractor_v3 import OwnershipExtractorV3, OwnershipRelationship


@dataclass
class GroundTruthShareholder:
    """Represents a ground truth shareholder"""
    name: str
    percentage: float
    type: str
    foreign: bool
    government: bool


def load_ground_truth() -> Dict[str, List[GroundTruthShareholder]]:
    """
    Load ground truth from ground_truth.md file.
    Returns a dictionary mapping sample names to ground truth shareholders.
    """
    ground_truth_file = '/data/Projects/bpm2007_ml_explorer-experiment/data/text_mining/ground_truth.md'

    with open(ground_truth_file, 'r') as f:
        content = f.read()

    # Parse ground truth from markdown tables
    samples = {}

    # Split into sample sections
    sample_sections = re.split(r'## Sample \d+:', content)

    for section in sample_sections[1:]:  # Skip header
        # Extract sample name and file
        sample_match = re.search(r'([^(]+)\s*\(([^)]+)\)', section)
        if not sample_match:
            continue

        sample_name = sample_match.group(1).strip()
        sample_file = sample_match.group(2).strip()

        # Find the table after "Ground Truth: Top 10 Shareholders"
        table_start = section.find('Ground Truth: Top 10 Shareholders')
        if table_start == -1:
            continue

        table_section = section[table_start:]
        table_end = table_section.find('\n###')
        if table_end == -1:
            table_end = len(table_section)

        table_section = table_section[:table_end]

        # Extract table rows (lines starting with | followed by a number)
        shareholders = []

        for line in table_section.split('\n'):
            line = line.strip()

            # Skip header row and separator
            if not line.startswith('|') or 'Rank' in line or '---' in line:
                continue

            # Parse table row: | 1 | Employees Provident Fund (EPF) | 35.25% | Direct/Beneficial | No | Yes |
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]  # Remove empty strings

            if len(parts) >= 6:
                try:
                    rank = parts[0]
                    name = parts[1]
                    percentage_str = parts[2]
                    share_type = parts[3]
                    foreign_str = parts[4]
                    government_str = parts[5]

                    # Extract percentage
                    pct_match = re.search(r'(\d+(?:\.\d+)?)', percentage_str)
                    if not pct_match:
                        continue

                    percentage = float(pct_match.group(1))
                    foreign = foreign_str.lower() == 'yes'
                    government = government_str.lower() == 'yes'

                    shareholders.append(GroundTruthShareholder(
                        name=name,
                        percentage=percentage,
                        type=share_type,
                        foreign=foreign,
                        government=government
                    ))
                except (ValueError, IndexError) as e:
                    # Skip malformed rows
                    continue

        if shareholders:
            samples[sample_file] = shareholders

    return samples


def normalize_name(name: str) -> str:
    """Normalize entity name for comparison"""
    name = name.upper()
    name = re.sub(r'\s+', ' ', name)
    name = name.strip(' -')
    return name


def match_shareholders(extracted: List[OwnershipRelationship],
                       ground_truth: List[GroundTruthShareholder],
                       tolerance: float = 0.5) -> Tuple[List[Tuple], List, List]:
    """
    Match extracted shareholders to ground truth.

    Returns:
        - matches: List of (extracted, ground_truth) tuples
        - false_positives: Extracted shareholders not in ground truth
        - false_negatives: Ground truth shareholders not extracted
    """
    matches = []
    false_positives = []
    false_negatives = ground_truth.copy()

    # Try to match each extracted shareholder
    for extracted_rel in extracted:
        matched = False

        # First try exact name match
        for gt_shareholder in false_negatives:
            if normalize_name(extracted_rel.shareholder) == normalize_name(gt_shareholder.name):
                matches.append((extracted_rel, gt_shareholder))
                false_negatives.remove(gt_shareholder)
                matched = True
                break

        # If no exact match, try fuzzy match with percentage tolerance
        if not matched:
            for gt_shareholder in false_negatives:
                # Check if percentage is close
                if abs(extracted_rel.percentage - gt_shareholder.percentage) <= tolerance:
                    # Check if names are similar (one is subset of other)
                    ext_name = normalize_name(extracted_rel.shareholder)
                    gt_name = normalize_name(gt_shareholder.name)

                    if ext_name in gt_name or gt_name in ext_name:
                        matches.append((extracted_rel, gt_shareholder))
                        false_negatives.remove(gt_shareholder)
                        matched = True
                        break

        if not matched:
            false_positives.append(extracted_rel)

    return matches, false_positives, false_negatives


def calculate_metrics(matches: List[Tuple],
                      false_positives: List,
                      false_negatives: List) -> Dict[str, float]:
    """Calculate precision, recall, and F1 score"""
    true_positives = len(matches)
    fp = len(false_positives)
    fn = len(false_negatives)

    precision = true_positives / (true_positives + fp) if (true_positives + fp) > 0 else 0.0
    recall = true_positives / (true_positives + fn) if (true_positives + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        'true_positives': true_positives,
        'false_positives': fp,
        'false_negatives': fn,
        'precision': precision * 100,
        'recall': recall * 100,
        'f1_score': f1 * 100
    }


def print_error_analysis(false_positives: List, false_negatives: List):
    """Print detailed error analysis"""
    if false_positives:
        print("\n  FALSE POSITIVES (Extracted but not in ground truth):")
        for fp in false_positives[:5]:  # Show first 5
            print(f"    - {fp.shareholder}: {fp.percentage}%")
        if len(false_positives) > 5:
            print(f"    ... and {len(false_positives) - 5} more")

    if false_negatives:
        print("\n  FALSE NEGATIVES (In ground truth but not extracted):")
        for fn in false_negatives[:5]:  # Show first 5
            print(f"    - {fn.name}: {fn.percentage}%")
        if len(false_negatives) > 5:
            print(f"    ... and {len(false_negatives) - 5} more")


def main():
    """Main validation function"""
    print("=" * 80)
    print("OWNERSHIP EXTRACTOR VALIDATION")
    print("=" * 80)
    print()

    # Load ground truth
    print("Loading ground truth...")
    ground_truth = load_ground_truth()
    print(f"Loaded ground truth for {len(ground_truth)} samples\n")

    # Initialize extractor
    extractor = OwnershipExtractorV3()

    # Results for each sample
    all_results = {}

    # Test each sample
    for sample_file, gt_shareholders in ground_truth.items():
        print(f"Testing: {sample_file}")
        print("-" * 80)

        # Read sample text
        sample_path = f'/data/Projects/bpm2007_ml_explorer-experiment/data/text_mining/{sample_file}'
        with open(sample_path, 'r') as f:
            text = f.read()

        # Extract using all methods
        list_rels = extractor.extract_ownership_from_list(text, "Test Company")
        table_rels = extractor.extract_ownership_from_table(text, "Test Company")
        narrative_rels = extractor.extract_ownership_from_narrative(text, "Test Company")

        # Combine and deduplicate
        all_extracted = list_rels + table_rels + narrative_rels
        seen = set()
        unique_extracted = []
        for rel in all_extracted:
            key = (normalize_name(rel.shareholder), rel.percentage)
            if key not in seen:
                seen.add(key)
                unique_extracted.append(rel)

        print(f"Extracted {len(unique_extracted)} unique shareholders")
        print(f"Ground truth has {len(gt_shareholders)} shareholders")

        # Match and calculate metrics
        matches, false_positives, false_negatives = match_shareholders(unique_extracted, gt_shareholders)
        metrics = calculate_metrics(matches, false_positives, false_negatives)

        print(f"\nResults:")
        print(f"  True Positives: {metrics['true_positives']}")
        print(f"  False Positives: {metrics['false_positives']}")
        print(f"  False Negatives: {metrics['false_negatives']}")
        print(f"  Precision: {metrics['precision']:.1f}%")
        print(f"  Recall: {metrics['recall']:.1f}%")
        print(f"  F1 Score: {metrics['f1_score']:.1f}%")

        # Print error analysis
        print_error_analysis(false_positives, false_negatives)

        # Store results
        all_results[sample_file] = metrics
        print()

    # Overall metrics
    print("=" * 80)
    print("OVERALL METRICS")
    print("=" * 80)

    total_tp = sum(r['true_positives'] for r in all_results.values())
    total_fp = sum(r['false_positives'] for r in all_results.values())
    total_fn = sum(r['false_negatives'] for r in all_results.values())

    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0.0

    print(f"\nTotal True Positives: {total_tp}")
    print(f"Total False Positives: {total_fp}")
    print(f"Total False Negatives: {total_fn}")
    print(f"\nOverall Precision: {overall_precision * 100:.1f}%")
    print(f"Overall Recall: {overall_recall * 100:.1f}%")
    print(f"Overall F1 Score: {overall_f1 * 100:.1f}%")

    # Performance evaluation
    print("\n" + "=" * 80)
    print("PERFORMANCE EVALUATION")
    print("=" * 80)

    if overall_f1 > 90:
        print("✅ EXCELLENT PERFORMANCE (> 90% F1 Score)")
    elif overall_f1 > 75:
        print("✅ GOOD PERFORMANCE (> 75% F1 Score)")
    elif overall_f1 > 60:
        print("⚠️ ACCEPTABLE PERFORMANCE (> 60% F1 Score)")
    else:
        print("❌ NEEDS IMPROVEMENT (< 60% F1 Score)")

    # Save results to JSON
    results_output = {
        'overall': {
            'precision': overall_precision * 100,
            'recall': overall_recall * 100,
            'f1_score': overall_f1 * 100,
            'true_positives': total_tp,
            'false_positives': total_fp,
            'false_negatives': total_fn
        },
        'samples': all_results
    }

    output_path = '/data/Projects/bpm2007_ml_explorer-experiment/data/text_mining/validation_results.json'
    with open(output_path, 'w') as f:
        json.dump(results_output, f, indent=2)

    print(f"\n✅ Results saved to: {output_path}")


if __name__ == "__main__":
    main()
