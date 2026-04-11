"""
Ownership Extraction Module
Extracts ownership relationships from Malaysian corporate documents using regex-based pattern matching.

Designed for:
- Annual reports
- Shareholder disclosure sections
- Corporate announcements

Target information:
- Shareholder names
- Ownership percentages
- Direct vs. ultimate ownership
- Control relationships (10%+ threshold)
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


class OwnershipExtractor:
    """Extracts ownership information from Malaysian corporate documents"""

    def __init__(self):
        # Patterns for Malaysian corporate documents
        self.percentage_patterns = [
            r'(\d+(?:\.\d+)?)\s*%',
            r'(\d+(?:\.\d+)?)\s*per\s*cent',
            r'(\d+(?:\.\d+)?)\s*pc',
        ]

        self.shareholder_patterns = [
            r'(?:principal|major|top)\s*(?:shareholders?|substantial\s*shareholders?)',
            r'shareholders?',
            r'substantial\s*shareholders?',
        ]

        self.direct_indirect_patterns = [
            r'(?:direct\s*and\s*indirect|direct|indirect)\s*interest',
            r'beneficial\s*owner',
            r'ultimate\s*shareholder',
        ]

    def extract_ownership_from_text(self, text: str, company_name: str = "") -> List[OwnershipRelationship]:
        """
        Extract ownership relationships from text.

        Args:
            text: Document text (e.g., annual report section)
            company_name: Name of the company being analyzed

        Returns:
            List of OwnershipRelationship objects
        """
        relationships = []

        # Find all percentage mentions
        percentages = self._extract_percentages(text)

        # Find shareholder names
        shareholder_names = self._extract_shareholder_names(text, percentages)

        # Create relationships
        for name, pct in shareholder_names:
            ownership_type = self._determine_ownership_type(text, name)

            relationship = OwnershipRelationship(
                shareholder=name,
                company=company_name,
                percentage=pct,
                ownership_type=ownership_type,
                source_text=self._extract_context(text, name, pct)
            )
            relationships.append(relationship)

        return relationships

    def _extract_percentages(self, text: str) -> List[Tuple[float, int]]:
        """Extract all percentages with their positions in text"""
        percentages = []

        for pattern in self.percentage_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                percentage = float(match.group(1))
                position = match.start()
                percentages.append((percentage, position))

        return sorted(percentages, key=lambda x: x[1])

    def _extract_shareholder_names(self, text: str, percentages: List[Tuple[float, int]]) -> List[Tuple[str, float]]:
        """Extract shareholder names associated with percentages"""
        shareholder_pct_pairs = []

        for percentage, position in percentages:
            # Look for entity name immediately before the percentage
            context_start = max(0, position - 200)
            context = text[context_start:position]

            # Try to find the name in several patterns
            # Pattern 1: "Name - XX.XX%" or "Name - XX.XX %" (with space)
            name_match = re.search(r'([A-Z][A-Za-z\s&\-\.]+(?:Bhd|Berhad|Sdn|Pte|Ltd|Inc|Corp|Holdings|Group|Fund))\s*[-—–]\s*', context)
            if name_match:
                name = name_match.group(1).strip()
                shareholder_pct_pairs.append((name, percentage))
                continue

            # Pattern 2: "Name (XX.XX%)"
            name_match = re.search(r'([A-Z][A-Za-z\s&\-\.]+(?:Bhd|Berhad|Sdn|Pte|Ltd|Inc|Corp|Holdings|Group|Fund))\s*\(\s*\d+', context)
            if name_match:
                name = name_match.group(1).strip()
                shareholder_pct_pairs.append((name, percentage))
                continue

            # Pattern 3: Last capitalized entity name before percentage
            # Find all entity names in context
            entity_matches = re.finditer(r'([A-Z][A-Za-z\s&\-\.]+(?:Bhd|Berhad|Sdn|Pte|Ltd|Inc|Corp|Holdings|Group|Fund))', context)
            names = [m.group(1).strip() for m in entity_matches]

            if names:
                # Take the last one (closest to percentage)
                name = names[-1]
                shareholder_pct_pairs.append((name, percentage))

        # Remove duplicates (keep first occurrence)
        seen = set()
        unique_pairs = []
        for name, pct in shareholder_pct_pairs:
            if (name, pct) not in seen:
                seen.add((name, pct))
                unique_pairs.append((name, pct))

        return unique_pairs

    def _determine_ownership_type(self, text: str, shareholder: str) -> OwnershipType:
        """Determine if ownership is direct, indirect, or beneficial"""
        # Find context around shareholder mention
        context = self._extract_context(text, shareholder, None, window=100)

        if 'beneficial' in context.lower():
            return OwnershipType.BENEFICIAL
        elif 'indirect' in context.lower():
            return OwnershipType.INDIRECT
        elif 'direct' in context.lower():
            return OwnershipType.DIRECT
        else:
            return OwnershipType.UNKNOWN

    def _extract_context(self, text: str, name: str, percentage: Optional[float], window: int = 150) -> str:
        """Extract context around a mention"""
        # Find position of name
        name_pos = text.find(name)
        if name_pos == -1:
            return ""

        context_start = max(0, name_pos - window)
        context_end = min(len(text), name_pos + len(name) + window)

        return text[context_start:context_end].strip()

    def filter_control_relationships(self, relationships: List[OwnershipRelationship], threshold: float = 10.0) -> List[OwnershipRelationship]:
        """
        Filter relationships by control threshold (BPM7: 10%+).

        Args:
            relationships: List of ownership relationships
            threshold: Minimum percentage for control (default 10%)

        Returns:
            Filtered list of control relationships
        """
        return [r for r in relationships if r.percentage >= threshold]

    def extract_direct_investment_candidates(self, relationships: List[OwnershipRelationship]) -> List[OwnershipRelationship]:
        """
        Identify candidates for direct investment classification.

        BPM7 criteria:
        - Direct investment: 10%+ ownership with control/influence
        - Consider ownership type (direct > indirect)
        - Consider percentage (higher = more likely DI)

        Returns:
            Candidates sorted by likelihood of being DI
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

        # Return top candidates
        return [rel for score, rel in scored if score >= 50]  # Threshold for DI likelihood

    def _is_foreign_entity(self, name: str) -> bool:
        """Heuristic to identify foreign entities"""
        foreign_indicators = [
            'Singapore', 'USA', 'UK', 'Japan', 'China', 'Hong Kong',
            'Pte', 'Ltd', 'Inc', 'Corp', 'LLC', 'Sarl', 'GmbH'
        ]

        return any(indicator in name for indicator in foreign_indicators)

    def _is_government_entity(self, name: str) -> bool:
        """Identify government/sovereign entities"""
        govt_indicators = [
            'Government', 'Ministry', 'Khazanah', 'EPF', 'KWAP',
            'Sovereign', 'State', 'Federal', 'National'
        ]

        return any(indicator in name for indicator in govt_indicators)


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
    extractor = OwnershipExtractor()

    # Extract from sample text
    sample_text = create_sample_malaysian_text()
    relationships = extractor.extract_ownership_from_text(sample_text, "ABC Berhad")

    print("=" * 70)
    print("EXTRACTED OWNERSHIP RELATIONSHIPS")
    print("=" * 70)

    for rel in relationships:
        print(f"\nShareholder: {rel.shareholder}")
        print(f"Company: {rel.company}")
        print(f"Percentage: {rel.percentage}%")
        print(f"Type: {rel.ownership_type.value}")
        print(f"Context: {rel.source_text[:100]}..." if rel.source_text else "No context")

    # Filter control relationships (10%+)
    print("\n" + "=" * 70)
    print("CONTROL RELATIONSHIPS (10%+ threshold)")
    print("=" * 70)

    control_rels = extractor.filter_control_relationships(relationships)
    for rel in control_rels:
        print(f"{rel.shareholder}: {rel.percentage}% ({rel.ownership_type.value})")

    # Identify DI candidates
    print("\n" + "=" * 70)
    print("DIRECT INVESTMENT CANDIDATES")
    print("=" * 70)

    di_candidates = extractor.extract_direct_investment_candidates(relationships)
    for rel in di_candidates:
        print(f"{rel.shareholder}: {rel.percentage}% ({rel.ownership_type.value})")
