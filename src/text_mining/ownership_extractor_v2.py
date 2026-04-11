"""
Ownership Extraction Module v2
Improved version that handles structured list formats better.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class OwnershipType(Enum):
    """Types of ownership relationships"""
    DIRECT = "direct"
    INDIRECT = "indirect"
    BENEFICIAL = "beneficial"
    UNKNOWN = "unknown"


@dataclass
class OwnershipRelationship:
    """Represents an ownership relationship"""
    shareholder: str
    company: str
    percentage: float
    ownership_type: OwnershipType
    shares: Optional[int] = None
    source_text: Optional[str] = None


class OwnershipExtractorV2:
    """Extracts ownership information from Malaysian corporate documents"""

    def __init__(self):
        self.control_threshold = 10.0  # BPM7 threshold for control

    def extract_ownership_from_list(self, text: str, company_name: str = "") -> List[OwnershipRelationship]:
        """
        Extract ownership from structured list format (e.g., "1. Name - XX.XX%").

        This is the most common format in Malaysian annual reports.
        """
        relationships = []

        # Improved pattern: more flexible entity name matching
        # Captures: "1. Name - XX.XX%" or "1. Name (ABBR) - XX.XX%"
        # Handles: Bhd, Berhad, Sdn, Pte, Ltd, Inc, Corp, Holdings, Group, Fund, Bank, (EPF), (KWAP), etc.
        list_pattern = r'(?:^\s*\d+[\.\)]\s*)([A-Z][A-Za-z\s&\-\.0-9\(\)]+?(?:Bhd|Berhad|Sdn|Pte|Ltd|Inc|Corp|Holdings|Group|Fund|Bank|Trust|Management|(?:\([A-Z]+\)))(?=\s*[-—–]\s*\d+(?:\.\d+)?\s*%)'

        for match in re.finditer(list_pattern, text, re.MULTILINE):
            name = match.group(1).strip()
            percentage = float(match.group(2))

        for match in re.finditer(list_pattern, text, re.MULTILINE):
            name = match.group(1).strip()
            percentage = float(match.group(2))

            ownership_type = self._determine_ownership_type(text, name)
            context = self._extract_line_context(text, match.start())

            relationship = OwnershipRelationship(
                shareholder=name,
                company=company_name,
                percentage=percentage,
                ownership_type=ownership_type,
                source_text=context
            )
            relationships.append(relationship)

        return relationships

    def extract_ownership_from_table(self, text: str, company_name: str = "") -> List[OwnershipRelationship]:
        """
        Extract ownership from table format (rows with shareholder and percentage).
        """
        relationships = []

        # Split into lines and look for table-like structures
        lines = text.split('\n')

        for line in lines:
            # Look for lines with percentage
            if '%' in line:
                # Extract percentage
                pct_match = re.search(r'(\d+(?:\.\d+)?)\s*%', line)
                if pct_match:
                    percentage = float(pct_match.group(1))

                    # Extract name (everything before the percentage, cleaned)
                    name_part = line[:pct_match.start()].strip()
                    name = self._clean_entity_name(name_part)

                    if name and len(name) > 3:  # Minimum name length
                        ownership_type = self._determine_ownership_type(text, name)

                        relationship = OwnershipRelationship(
                            shareholder=name,
                            company=company_name,
                            percentage=percentage,
                            ownership_type=ownership_type,
                            source_text=line.strip()
                        )
                        relationships.append(relationship)

        return relationships

    def _clean_entity_name(self, name: str) -> str:
        """Clean and extract entity name from text"""
        # Remove common prefixes
        name = re.sub(r'^(?:Shareholder|Name|Entity|Company)\s*:?\s*', '', name, flags=re.IGNORECASE)

        # Remove numbering
        name = re.sub(r'^\d+[\.\)]\s*', '', name)

        # Remove trailing punctuation and whitespace
        name = name.strip(' -—–\t\n\r')

        return name

    def _determine_ownership_type(self, text: str, shareholder: str) -> OwnershipType:
        """Determine if ownership is direct, indirect, or beneficial"""
        # Find context around shareholder mention (broader search)
        context = self._extract_context(text, shareholder, window=300)

        context_lower = context.lower()

        if 'beneficial' in context_lower and 'owner' in context_lower:
            return OwnershipType.BENEFICIAL
        elif 'indirect' in context_lower:
            return OwnershipType.INDIRECT
        elif 'direct' in context_lower:
            return OwnershipType.DIRECT
        else:
            return OwnershipType.UNKNOWN

    def _extract_context(self, text: str, name: str, window: int = 150) -> str:
        """Extract context around a mention"""
        # Find all positions of the name
        positions = []
        start = 0
        while True:
            pos = text.find(name, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1

        if not positions:
            return ""

        # Extract context around each position and combine
        contexts = []
        for pos in positions:
            context_start = max(0, pos - window)
            context_end = min(len(text), pos + len(name) + window)
            contexts.append(text[context_start:context_end])

        return " ... ".join(contexts)

    def _extract_line_context(self, text: str, position: int) -> str:
        """Extract the full line containing a position"""
        line_start = text.rfind('\n', 0, position) + 1
        line_end = text.find('\n', position)
        if line_end == -1:
            line_end = len(text)

        return text[line_start:line_end].strip()

    def filter_control_relationships(self, relationships: List[OwnershipRelationship]) -> List[OwnershipRelationship]:
        """Filter relationships by control threshold (BPM7: 10%+)."""
        return [r for r in relationships if r.percentage >= self.control_threshold]

    def extract_direct_investment_candidates(self, relationships: List[OwnershipRelationship]) -> List[OwnershipRelationship]:
        """
        Identify candidates for direct investment classification.

        BPM7 criteria:
        - Direct investment: 10%+ ownership with control/influence
        """
        # Filter by 10% threshold
        control_relationships = self.filter_control_relationships(relationships)

        # Score each relationship for DI likelihood
        scored = []
        for rel in control_relationships:
            score = 0

            # Higher percentage = more likely DI
            score += min(rel.percentage / 100, 1.0) * 40

            # Direct ownership > Indirect > Beneficial
            if rel.ownership_type == OwnershipType.DIRECT:
                score += 30
            elif rel.ownership_type == OwnershipType.INDIRECT:
                score += 15
            elif rel.ownership_type == OwnershipType.BENEFICIAL:
                score += 10

            # Foreign-sounding names (heuristic)
            if self._is_foreign_entity(rel.shareholder):
                score += 20

            # Government/sovereign entities (likely strategic)
            if self._is_government_entity(rel.shareholder):
                score += 10

            scored.append((score, rel))

        # Sort by score (descending)
        scored.sort(key=lambda x: x[0], reverse=True)

        # Return top candidates (score >= 50)
        return [rel for score, rel in scored if score >= 50]

    def _is_foreign_entity(self, name: str) -> bool:
        """Heuristic to identify foreign entities"""
        foreign_indicators = [
            'Singapore', 'USA', 'UK', 'Japan', 'China', 'Hong Kong',
            'Pte', 'Inc', 'LLC', 'Sarl', 'GmbH', 'SAS', 'SA'
        ]

        return any(indicator in name for indicator in foreign_indicators)

    def _is_government_entity(self, name: str) -> bool:
        """Identify government/sovereign entities"""
        govt_indicators = [
            'Khazanah', 'EPF', 'KWAP', 'Government', 'Ministry',
            'Sovereign', 'State', 'Federal', 'National', 'Fund'
        ]

        return any(indicator in name for indicator in govt_indicators)

    def analyze_completeness(self, relationships: List[OwnershipRelationship]) -> Dict:
        """Analyze the completeness of extracted ownership data"""
        if not relationships:
            return {
                'total_shareholders': 0,
                'total_percentage': 0.0,
                'control_threshold_met': False,
                'completeness_score': 0.0,
                'foreign_owners': 0,
                'government_owners': 0
            }

        total_pct = sum(r.percentage for r in relationships)
        foreign_owners = sum(1 for r in relationships if self._is_foreign_entity(r.shareholder))
        government_owners = sum(1 for r in relationships if self._is_government_entity(r.shareholder))
        control_threshold_met = any(r.percentage >= self.control_threshold for r in relationships)

        # Completeness: how close to 100% ownership?
        completeness_score = min(total_pct / 100.0, 1.0) * 100

        return {
            'total_shareholders': len(relationships),
            'total_percentage': total_pct,
            'control_threshold_met': control_threshold_met,
            'completeness_score': completeness_score,
            'foreign_owners': foreign_owners,
            'government_owners': government_owners
        }


def create_sample_malaysian_text() -> str:
    """Create sample text from Malaysian annual report for testing"""
    return """
    PRINCIPAL SHAREHOLDERS

    As at 31 December 2025, the principal shareholders of ABC Berhad are:

    1. Singapore Holdings Pte Ltd - 25.5%
    2. Malaysian Investment Holdings Berhad - 18.2%
    3. Khazanah Nasional Berhad - 12.0%
    4. Global Capital Investors Inc - 8.5%
    5. EPF (Employees Provident Fund) - 6.0%

    SUBSTANTIAL SHAREHOLDERS

    Singapore Holdings Pte Ltd holds 25.5% of the issued share capital
    through direct and indirect interests. The beneficial owner is Singapore
    Government Investment Corporation Pte Ltd.

    Malaysian Investment Holdings Berhad holds a direct interest of 18.2%
    in ABC Berhad and is the ultimate parent company.

    Khazanah Nasional Berhad holds 12.0% as a strategic investment.

    Shareholders holding more than 5% of the issued share capital are
    required to disclose their interests under the Companies Act 2016.
    """


if __name__ == "__main__":
    # Test the extractor
    extractor = OwnershipExtractorV2()

    # Extract from sample text
    sample_text = create_sample_malaysian_text()

    print("=" * 70)
    print("EXTRACTING FROM LIST FORMAT")
    print("=" * 70)
    relationships = extractor.extract_ownership_from_list(sample_text, "ABC Berhad")

    for rel in relationships:
        print(f"\n{rel.shareholder}")
        print(f"  Percentage: {rel.percentage}%")
        print(f"  Type: {rel.ownership_type.value}")
        print(f"  Source: {rel.source_text[:80]}...")

    # Analyze completeness
    print("\n" + "=" * 70)
    print("COMPLETENESS ANALYSIS")
    print("=" * 70)

    analysis = extractor.analyze_completeness(relationships)
    for key, value in analysis.items():
        print(f"{key}: {value}")

    # Filter control relationships
    print("\n" + "=" * 70)
    print(f"CONTROL RELATIONSHIPS ({extractor.control_threshold}%+ threshold)")
    print("=" * 70)

    control_rels = extractor.filter_control_relationships(relationships)
    for rel in control_rels:
        foreign_marker = " [FOREIGN]" if extractor._is_foreign_entity(rel.shareholder) else ""
        govt_marker = " [GOVT]" if extractor._is_government_entity(rel.shareholder) else ""
        print(f"{rel.shareholder}: {rel.percentage}% ({rel.ownership_type.value}){foreign_marker}{govt_marker}")

    # Identify DI candidates
    print("\n" + "=" * 70)
    print("DIRECT INVESTMENT CANDIDATES")
    print("=" * 70)

    di_candidates = extractor.extract_direct_investment_candidates(relationships)
    for rel in di_candidates:
        print(f"{rel.shareholder}: {rel.percentage}% ({rel.ownership_type.value})")

    if not di_candidates:
        print("(No DI candidates meet the threshold)")
