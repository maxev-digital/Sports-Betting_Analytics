# NCAA Team Name Mappings Reference

## Sports Data IO Abbreviations to Full Names

This document provides a comprehensive reference for all NCAA team abbreviations used by the Sports Data IO API.

### Basketball (NCAAB) & Football (NCAAF) Teams

| Abbreviation | Full Team Name |
|--------------|----------------|
| ABCHR | Abilene Christian |
| ALCST | Alcorn State |
| APPLST | Appalachian State |
| ARPB | Arkansas-Pine Bluff |
| AUBRN | Auburn |
| BCOOK | Bethune-Cookman |
| BOSCOL | Boston College |
| CAH | Charleston |
| CAMP | Campbell |
| CENCON | Central Connecticut |
| CHIST | Charleston Southern |
| CITA | The Citadel |
| CSUNR | Cal State Northridge |
| DEN | Denver |
| DRAKE | Drake |
| FL | Florida |
| GAS | Georgia Southern |
| GRMBST | Grambling State |
| ILLST | Illinois State |
| IOWAST | Iowa State |
| IUPUI | IUPUI |
| JACKST | Jackson State |
| LEMYN | Le Moyne |
| LIUB | Long Island University |
| LOU | Louisville |
| LOYCH | Loyola Chicago |
| MERRI | Merrimack |
| MIA | Miami |
| MRCY | Mercy |
| NDAK | North Dakota |
| NEOM | New Mexico |
| NFL | Niagara Falls |
| NIOWA | Northern Iowa |
| NTX | North Texas |
| NWST | Northwestern State |
| OHIO | Ohio |
| PORT | Portland |
| QUIN | Quincy |
| ROBMS | Robert Morris |
| SALA | Salisbury |
| SFL | South Florida |
| SMU | SMU |
| STFPA | St. Francis (PA) |
| STLOU | Saint Louis |
| TAMU | Texas A&M |
| TCU | TCU |
| TXAM | Texas A&M (alternate) |
| TXS | Texas Southern |
| UCRVS | UC Riverside |
| UTSA | UT San Antonio |
| WASH | Washington |
| WRGHT | Wright State |
| WVIR | West Virginia |
| XAV | Xavier |

## Implementation Files

- **C:\Users\nashr\frontend\src\utils\ncaaTeamMappings.ts** - Standalone NCAA mappings file
- **C:\Users\nashr\frontend\src\utils\teamNames.ts** - Updated to integrate NCAA mappings

## Usage Examples

### TypeScript/JavaScript

```typescript
import { getNCAATeamName } from './utils/ncaaTeamMappings';

// Get basketball team name
const teamName = getNCAATeamName('APPLST', 'basketball');
console.log(teamName); // "Appalachian State"

// Get football team name
const footballTeam = getNCAATeamName('AUBRN', 'football');
console.log(footballTeam); // "Auburn"
```

### Using formatTeamName from teamNames.ts

```typescript
import { formatTeamName } from './utils/teamNames';

// NCAA Basketball
const ncaabTeam = formatTeamName('IOWAST', 'basketball_ncaab');
console.log(ncaabTeam); // "Iowa State"

// NCAA Football
const ncaafTeam = formatTeamName('BOSCOL', 'americanfootball_ncaaf');
console.log(ncaafTeam); // "Boston College"
```

## Notes

- **TAMU vs TXAM**: Both abbreviations map to "Texas A&M" (different sources may use either)
- **GAS**: Georgia Southern (not Georgia State)
- **SFL**: South Florida (not San Francisco)
- **WVIR**: West Virginia (full state, not just "Virginia")
- **NFL**: Niagara Falls (not the professional league)
- **IUPUI**: Kept as-is (Indiana University-Purdue University Indianapolis)

## Conference Breakdown (Sampled Teams)

### Power Conferences
- **ACC**: Boston College, Louisville, Miami, Florida State
- **Big 12**: Iowa State, TCU, West Virginia
- **SEC**: Auburn, Florida, Texas A&M
- **American**: SMU, South Florida, Memphis

### Mid-Major Conferences
- **SWAC**: Alcorn State, Grambling State, Jackson State, Arkansas-Pine Bluff
- **Southland**: Incarnate Word, McNeese, Northwestern State
- **Summit**: North Dakota, North Dakota State, Denver, Omaha
- **NEC**: Central Connecticut, LIU, Merrimack, St. Francis (PA)

## Data Source

These mappings are based on Sports Data IO's official team abbreviation system for NCAA Basketball (NCAAB) and NCAA Football (NCAAF) APIs.

Last Updated: 2025-11-06
