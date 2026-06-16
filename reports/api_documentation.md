## API Documentation and Data Source Strategy

### Purpose

The Global Data Careers Intelligence Platform integrates multiple external data sources to create a unified labor-market intelligence system. Each source contributes different information required to answer business questions related to job demand, salary trends, skill requirements, remote hiring patterns, and career recommendations.

The objective of using multiple APIs is to reduce reliance on a single source while improving coverage, accuracy, and analytical depth.

### RemoteOK API

Primary Purpose: Remote Hiring Intelligence

Primary Contribution:

* Remote job availability
* Remote work trends
* Global technology-focused hiring activity

Business Questions Supported:

* Which countries offer the most remote data roles?
* Which data roles are most frequently offered remotely?
* How does remote hiring vary by geography?

Strengths:

* Strong remote-job coverage
* Technology-focused opportunities
* Frequently updated listings

Limitations:

* Limited salary coverage
* Inconsistent industry classification

### Adzuna API

Primary Purpose: Salary and Labor Market Intelligence

Primary Contribution:

* Salary information
* Industry classification
* Location information
* Job descriptions

Business Questions Supported:

* Which tools are linked to higher salaries?
* Which industries hire the most data professionals?
* Which countries offer the strongest salary potential?

Strengths:

* Rich salary information
* Large job volume
* Detailed metadata

Limitations:

* Uneven coverage across countries

### USAJobs API

Primary Purpose: Structured Role Intelligence

Primary Contribution:

* Standardized job titles
* Detailed job descriptions
* Consistent role metadata

Business Questions Supported:

* What separates junior, mid-level, and senior roles?
* Which skills are associated with different role categories?
* How do requirements vary by role?

Strengths:

* Highly structured data
* Consistent metadata quality

Limitations:

* Government-focused labor market

### World Bank API

Primary Purpose: Economic Context

Primary Contribution:

* GDP per capita
* Unemployment rates
* Income group classifications
* Regional classifications

Business Questions Supported:

* Which countries offer the best opportunity-to-salary balance?
* How does economic context affect career opportunities?

Strengths:

* Global coverage
* Reliable economic indicators

Limitations:

* Does not provide labor-market job postings

### Data Ownership Rules

Salary Data:
Adzuna → USAJobs → RemoteOK

Location Data:
Adzuna → USAJobs → RemoteOK

Remote Status:
RemoteOK → Adzuna → USAJobs

Economic Context:
World Bank Only

### Initial Role Scope

The project focuses on:

* Data Analyst
* Business Intelligence Analyst
* BI Analyst
* Data Engineer
* Analytics Engineer
* Data Scientist
* Reporting Analyst
* Business Analyst (Data-focused only)

Roles outside the data-career pathway are excluded from analysis.

### Expected Business Value

The combined data sources provide a foundation for analyzing global data-career opportunities, identifying high-demand skills, measuring salary potential, evaluating remote hiring trends, and generating career recommendations for entry-level and junior professionals.

### Future Data Sources

Potential future integrations include:
- Indeed
- LinkedIn Jobs
- Glassdoor
- Levels.fyi

These are excluded from Version 1 to maintain project scope and API reliability.

### Source Failure Handling

If one source becomes unavailable:

1. RemoteOK Failure: Remote analysis unavailable but salary and skill analysis continue.

2. Adzuna Failure: Salary analysis becomes limited while remote and role analysis remain available.

3. USAJobs Failure: Role metadata coverage decreases but overall analysis remains operational.

4. World Bank Failure: Opportunity Score excludes economic indicators until refresh succeeds.

### Field Extraction Matrix
| Standard Field    | RemoteOK | Adzuna | USAJobs | World Bank |
| ----------------- | -------- | ------ | ------- | ---------- |
| job_id            | ✓        | ✓      | ✓       |            |
| job_title         | ✓        | ✓      | ✓       |            |
| company           | ✓        | ✓      |         |            |
| country           | ✓        | ✓      | ✓       |            |
| city              |          | ✓      | ✓       |            |
| salary_min        |          | ✓      | ✓       |            |
| salary_max        |          | ✓      | ✓       |            |
| description       | ✓        | ✓      | ✓       |            |
| remote_status     | ✓        | ✓      |         |            |
| posted_date       | ✓        | ✓      | ✓       |            |
| gdp_per_capita    |          |        |         | ✓          |
| unemployment_rate |          |        |         | ✓          |
| income_group      |          |        |         | ✓          |