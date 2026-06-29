# Raw Data Archive Strategy

## Purpose

The raw data archive stores original API responses before cleaning, transformation, or normalization. This protects the credibility of the project because every cleaned field can be traced back to its original source.

## Archive Location

Raw API responses are stored in:

data/raw/

## File Naming Convention

Each file uses the source name and extraction date.

Examples:

remoteok_YYYY_MM_DD.json  
adzuna_gb_YYYY_MM_DD.json  
usajobs_YYYY_MM_DD.json  
worldbank_YYYY_MM_DD.json  

## Sources Archived

- RemoteOK
- Adzuna
- USAJobs
- World Bank

## Rules

Raw files must not be manually edited.
Raw files must not be overwritten.
Raw files must not be committed to GitHub.
All cleaning must happen after raw archiving.
Raw files are immutable and serve as the system of record. All cleaning,
normalization, enrichment, and transformation must be performed on copies of
the raw data rather than modifying the archived files.

## Business Value

The archive allows the project to validate transformations, investigate errors, reproduce analysis, and prove where every cleaned field came from.