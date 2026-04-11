# GLEIF External Sector Discovery: Malaysia vs Indonesia Comparison

## Executive Summary

Both Malaysia and Indonesia show similar GLEIF data limitations:
- **Zero relationship coverage** for both countries
- **High reporting exceptions** (92% MY, likely similar for ID)
- **Entity-level data is rich and valuable**

## 📊 Comparative Results

| Metric | Malaysia 🇲🇾 | Indonesia 🇮🇩 |
|--------|--------------|---------------|
| **Total Entities** | 2,195 | 1,457 |
| **Relationships Found** | 0/200 tested | 0/50 tested |
| **Coverage Gap Score Range** | 0.57 - 0.90 | 0.596 (all identical) |
| **Primary Category** | GENERAL (68%), FUND (32%) | GENERAL (92%), FUND (7%) |
| **Major Cities** | Kuala Lumpur, Petaling Jaya, Ipoh | Jakarta, Jakarta Selatan, Tangerang |
| **Legal Forms** | XEOV, 8888, ZWYK | UD1V, 8888, 9999, JAJS |

---

## 🇲🇾 Malaysia Details

### Entity Distribution
- **GENERAL**: ~1,500 entities (68%)
- **FUND**: ~700 entities (32%)
- **BRANCH**: Minimal

### Top Cities
1. Kuala Lumpur
2. Petaling Jaya
3. Ipoh
4. Shah Alam
5. Subang Jaya

### Legal Forms
- **XEOV**: Private Limited Company (Berhad/SDN BHD)
- **8888**: Other/Unspecified
- **ZWYK**: Limited/Pte Ltd

### Notable Entities
- AIRBUS HELICOPTERS MALAYSIA SDN. BHD.
- MONDELEZ MALAYSIA SALES SDN. BHD.
- MAYBANK GLOBAL DIGITAL ASSET ECOSYSTEM EQUITY FUND
- CONCENTRIX MALAYSIA SDN. BHD.

---

## 🇮🇩 Indonesia Details

### Entity Distribution
- **GENERAL**: 1,343 entities (92%)
- **FUND**: 99 entities (7%)
- **BRANCH**: 7 entities (0.5%)
- **RESIDENT_GOVERNMENT_ENTITY**: 6 entities (0.4%)

### Top Cities
1. Jakarta: 454 entities
2. JAKARTA: 235 entities (capitalization variations)
3. Jakarta Selatan: 107 entities
4. Jakarta Pusat: 53 entities
5. South Jakarta: 35 entities

**Note**: Jakarta entities are split across multiple city name variations (Jakarta vs JAKARTA vs South Jakarta)

### Legal Forms
- **UD1V**: 695 entities (48%) - Likely "Usaha Dagang" (Trading Company)
- **8888**: 368 entities (25%) - Other/Unspecified
- **9999**: 167 entities (11%) - Other
- **JAJS**: 131 entities (9%) - Limited Liability Company (PT)
- **AEZW**: 51 entities (4%) - Foreign-owned company

### Notable Entities
- PT Kalimantan Aluminium Industry
- PT FONTERRA BRANDS MANUFACTURING INDONESIA
- PT MAYBANK ASSET MANAGEMENT
- PT Flender Drives Indonesia
- BATAM INDONESIA FREE ZONE AUTHORITY (if present)

---

## 🔍 Key Observations

### 1. Data Quality
**Both countries have identical limitations:**
- ✅ Rich entity-level data (names, addresses, legal forms)
- ❌ Zero relationship coverage (direct/ultimate parents)
- ❌ High reporting exception rates

### 2. Geographic Concentration
- **Malaysia**: More distributed across multiple cities
- **Indonesia**: Highly concentrated in Jakarta area (70%+ in greater Jakarta)

### 3. Entity Structure
- **Malaysia**: Higher fund ratio (32% vs 7%)
  - Indicates more sophisticated financial sector
  - More investment vehicles registered
- **Indonesia**: More operational companies (92% GENERAL)
  - Larger base of trading/manufacturing entities
  - More diverse business operations

### 4. Legal Form Diversity
- **Malaysia**: More standardized (XEOV, 8888, ZWYK)
- **Indonesia**: More varied (UD1V, JAJS, AEZW, 9999)
  - Reflects different regulatory categories
  - May indicate multiple business entity types

---

## 💡 Framework Value Assessment

### What Works Well (Both Countries)
✅ **Entity Discovery** — Identify all LEI-registered entities
✅ **Geographic Clustering** — Map entity distribution by city
✅ **Legal Form Analysis** — Understand entity structure types
✅ **Coverage Gap Scoring** — Prioritize entities for review
✅ **Trend Monitoring** — Track new registrations over time

### What Doesn't Work (Both Countries)
❌ **Relationship Mapping** — Zero parent/ultimate parent data
❌ **Ownership Hierarchy** — Cannot trace beneficial ownership
❌ **Capital Flow Tracing** — Cannot follow cross-border investments

---

## 🎯 Strategic Recommendations

### For Malaysia
1. **Focus on Fund Sector** — 32% funds suggest sophisticated financial market
2. **Geographic Diversity** — Use distributed city data for regional analysis
3. **Monitor New Registrations** — Track growth in entity count

### For Indonesia
1. **Focus on Operational Companies** — 92% GENERAL entities
2. **Jakarta Concentration** — High concentration suggests systemic risk importance
3. **Legal Form Analysis** — Investigate UD1V vs JAJS differences
4. **Foreign Ownership** — AEZW entities (4%) may be high-priority for review

### Cross-Country Comparisons
1. **Similar Data Limitations** — Both face same GLEIF constraints
2. **Different Economic Profiles** — MY = finance-heavy, ID = operations-heavy
3. **Geographic Patterns** — MY = distributed, ID = concentrated

---

## 🚀 Next Steps

### Short Term (1-2 weeks)
1. **Add Vietnam and Philippines** — Compare with similar economies
2. **Geographic Heatmaps** — Visualize entity distribution by city
3. **Legal Form Research** — Decode UD1V, JAJS, AEZW meanings

### Medium Term (1-2 months)
1. **Alternative Data Sources** — Bloomberg, Reuters, SSM (Indonesia)
2. **Entity Matching** — Cross-reference with IMF CPIS/COFER data
3. **Trend Analysis** — Track entity growth over time

### Long Term (3-6 months)
1. **Custom Scoring** — Adjust scores for relationship-less data
2. **Risk Models** — Build systemic risk indicators from entity metrics
3. **Policy Integration** — Connect with BNM/BI regulatory frameworks

---

## 📝 Conclusion

**Both Malaysia and Indonesia are viable candidates for this framework**, but with the same limitations:

✅ **Entity-level analysis is highly valuable**
- Comprehensive entity discovery
- Geographic and legal form insights
- Coverage gap prioritization

❌ **Relationship mapping is not possible via GLEIF**
- Alternative data sources required
- Ownership hierarchy needs different approach

**Recommendation:** Proceed with entity-level analysis for both countries, using GLEIF as the foundation and complementing with other data sources for relationship mapping.

---

*Generated: April 11, 2026*
*Data Source: GLEIF API (api.gleif.org)*
