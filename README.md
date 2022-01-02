# Academic genealogy scraper

```
pip install -r requirements.txt
python scrape.py id outfile.dot
```

where

- `id` is a numeric id, e.g., 20751
- `outfile.dot` is the DOT file to write to

Then to convert to (say) PDF, do:

```
dot -Tpdf outfile.dot -o outfile.pdf
```
