# Accessing All Prior Versions of `USDT_NNDSS_data.csv`

This document describes how to retrieve every historical version of
[`USDT_NNDSS_data.csv`](USDT_NNDSS_data.csv) (in this `data/` folder) from this
repository, using either plain `git`, Python, or R.

## Method 1: git (recommended if you have the repo cloned)

List every commit that touched the file, then extract each version:

```bash
git log --follow --format="%H %ai" -- data/USDT_NNDSS_data.csv > commit_list.txt

mkdir -p versions
while read -r sha date rest; do
  git show "$sha:data/USDT_NNDSS_data.csv" > "versions/${sha}.csv" 2>/dev/null
done < commit_list.txt
```

No GitHub API token is required since this runs entirely on your local clone.

## Method 2: GitHub API (Python)

Useful if you don't want to clone the full repository.

```python
import requests, base64, os

OWNER, REPO, PATH = "USDiseaseTracker", "USDT", "data/USDT_NNDSS_data.csv"
TOKEN = os.environ.get("GITHUB_TOKEN")  # optional for public repos, recommended for rate limits
HEADERS = {"Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"

# 1. List all commits that touched this file
commits = []
page = 1
while True:
    r = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/commits",
        headers=HEADERS,
        params={"path": PATH, "per_page": 100, "page": page},
    )
    data = r.json()
    if not data:
        break
    commits.extend(data)
    page += 1

# 2. Fetch file content at each commit SHA
os.makedirs("versions", exist_ok=True)
for c in commits:
    sha = c["sha"]
    r = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{PATH}",
        headers=HEADERS,
        params={"ref": sha},
    )
    content_b64 = r.json().get("content")
    if content_b64:
        content = base64.b64decode(content_b64)
        with open(f"versions/{sha}.csv", "wb") as f:
            f.write(content)
```

Alternative for raw content (no base64 decoding, no auth needed for public repos):

```
https://raw.githubusercontent.com/USDiseaseTracker/USDT/{sha}/data/USDT_NNDSS_data.csv
```

## Method 3: GitHub API (R)

Using `httr`, `jsonlite`, and `base64enc`:

```r
library(httr)
library(jsonlite)
library(base64enc)

owner <- "USDiseaseTracker"; repo <- "USDT"; path <- "data/USDT_NNDSS_data.csv"
token <- Sys.getenv("GITHUB_TOKEN")  # optional for public repos
headers <- add_headers(Authorization = paste("token", token),
                        Accept = "application/vnd.github+json")

# 1. List all commits touching this file
commits <- list()
page <- 1
repeat {
  resp <- GET(sprintf("https://api.github.com/repos/%s/%s/commits", owner, repo),
              headers, query = list(path = path, per_page = 100, page = page))
  data <- content(resp, as = "parsed", simplifyVector = FALSE)
  if (length(data) == 0) break
  commits <- c(commits, data)
  page <- page + 1
}

# 2. Fetch file content at each SHA
dir.create("versions", showWarnings = FALSE)
for (c in commits) {
  sha <- c$sha
  resp <- GET(sprintf("https://api.github.com/repos/%s/%s/contents/%s", owner, repo, path),
              headers, query = list(ref = sha))
  file_data <- content(resp, as = "parsed", simplifyVector = FALSE)
  if (!is.null(file_data$content)) {
    raw_content <- rawToChar(base64decode(gsub("\n", "", file_data$content)))
    writeLines(raw_content, sprintf("versions/%s.csv", sha))
  }
}
```

Or more simply with the `gh` package:

```r
library(gh)
commits <- gh("/repos/{owner}/{repo}/commits", owner = "USDiseaseTracker", repo = "USDT",
              path = "data/USDT_NNDSS_data.csv", .limit = Inf)
```

## Notes

- Unauthenticated GitHub API requests are capped at 60/hour; a personal access token
  (set as the `GITHUB_TOKEN` environment variable) raises this to 5,000/hour.
- `git log --follow` also tracks file renames, which the API `path` parameter does not
  always catch consistently.
- Each extracted version is saved to a `versions/` directory, named by commit SHA.
