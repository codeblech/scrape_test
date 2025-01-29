# Speed Tests

## Jina.ai Scraping Test Results

| Site | Mean Time (s) | 95% CI | Min-Max (s) |
|------|---------------|---------|-------------|
| Wikipedia (Reference) | 7.0220 | ±2.0670 | 4.1411-11.1746 |
| JS Rendered | 0.7510 | ±0.1016 | 0.6250-0.9293 |
| Table Layout | 0.8141 | ±0.0682 | 0.6661-0.8973 |
| Pagination | 0.8561 | ±0.1849 | 0.6263-1.2478 |
| Infinite Scroll | 0.8167 | ±0.1649 | 0.6231-1.1639 |
|------|---------------|---------|-------------|
| **Total Mean** | **10.2599** | | |

### Details
Number of iterations per URL: 5

## Crawlee Scraping Test Results

| Site | Mean Time (s) | 95% CI | Min-Max (s) |
|------|---------------|---------|-------------|
| Wikipedia (Reference) | 0.6154 | ±0.9637 | 0.0559-2.8142 |
| JS Rendered | 0.4078 | ±0.5952 | 0.0412-1.7641 |
| Table Layout | 0.3359 | ±0.4739 | 0.0519-1.4170 |
| Pagination | 0.2306 | ±0.3011 | 0.0503-0.9176 |
| Infinite Scroll | 0.2618 | ±0.3713 | 0.0420-1.1090 |
|------|---------------|---------|-------------|
| **Total Mean** | **1.8515** | | |

### Details
Number of iterations per URL: 5

## Crawlee Scraping Test Results (conversion to Markdown time included, markitdown)

| Site | Mean Time (s) | 95% CI | Min-Max (s) |
|------|---------------|---------|-------------|
| Wikipedia (Reference) | 0.4010 | ±0.6225 | 0.0420-1.8215 |
| JS Rendered | 0.3127 | ±0.4685 | 0.0386-1.3817 |
| Table Layout | 0.3159 | ±0.4878 | 0.0326-1.4290 |
| Pagination | 0.1999 | ±0.2839 | 0.0341-0.8476 |
| Infinite Scroll | 1.2104 | ±2.0667 | 0.0284-5.9261 |
|------|---------------|---------|-------------|
| **Total Mean** | **2.4399** | | |

### Details
Number of iterations per URL: 5


## Crawlee Scraping Test Results (using headless browser, conversion to Markdown time included, markitdown)

| Site | Mean Time (s) | 95% CI | Min-Max (s) |
|------|---------------|---------|-------------|
| Wikipedia (Reference) | 0.9407 | ±1.0618 | 0.2977-3.3626 |
| JS Rendered | 0.9932 | ±1.2036 | 0.2990-3.7393 |
| Table Layout | 0.8547 | ±0.9534 | 0.3042-3.0300 |
| Pagination | 0.9454 | ±0.7115 | 0.5316-2.5688 |
| Infinite Scroll | 1.0272 | ±0.8851 | 0.5120-3.0468 |
|------|---------------|---------|-------------|
| **Total Mean** | **4.7611** | | |

### Details
Number of iterations per URL: 5

# Crawlee Scraping Test Results (using headless browser, conversion to Markdown time included, markdownify)

| Site | Mean Time (s) | 95% CI | Min-Max (s) |
|------|---------------|---------|-------------|
| Wikipedia (Reference) | 0.9076 | ±1.0760 | 0.2782-3.3624 |
| JS Rendered | 1.0413 | ±1.3255 | 0.2798-4.0657 |
| Table Layout | 0.8698 | ±0.9978 | 0.2927-3.1464 |
| Pagination | 0.7086 | ±0.7203 | 0.2843-2.3516 |
| Infinite Scroll | 0.8052 | ±0.9199 | 0.2745-2.9040 |
|------|---------------|---------|-------------|
| **Total Mean** | **4.3326** | | |

## Details
Number of iterations per URL: 5



## Docling Scraping Test Results

| Site | Mean Time (s) | 95% CI | Min-Max (s) |
|------|---------------|---------|-------------|
| Wikipedia (Reference) | 2.2060 | ±0.1683 | 2.0566-2.5674 |
| JS Rendered | 1.7465 | ±0.3135 | 1.4533-2.3896 |
| Table Layout | 1.4070 | ±0.0499 | 1.3293-1.4887 |
| Pagination | 1.1382 | ±0.0068 | 1.1248-1.1443 |
| Infinite Scroll | 0.9453 | ±0.1063 | 0.7599-1.1119 |
|------|---------------|---------|-------------|
| **Total Mean** | **7.4430** | | |

### Details
Number of iterations per URL: 5

## URLs
"Wikipedia (Reference)": "en.wikipedia.org/wiki/Formula_One" \
"JS Rendered": "quotes.toscrape.com/js" \
"Table Layout": "quotes.toscrape.com/tableful" \
"Pagination": "quotes.toscrape.com" \
"Infinite Scroll": "quotes.toscrape.com/scroll"
