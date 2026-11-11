#!/usr/bin/env python3
"""doc_tables.py — from a saved read_doc JSON, print the page text width and each
table's startIndex, column count and current widths (for fit_columns.py)."""
import json, sys
d = json.load(open(sys.argv[1]))
d = d.get("content", d)
tab = d["tabs"][0]["documentTab"] if "tabs" in d else d
ds = tab["documentStyle"]
mag = lambda x: (x or {}).get("magnitude", 0)
width = mag(ds["pageSize"]["width"]) - mag(ds.get("marginLeft")) - mag(ds.get("marginRight"))
def equations(els, out):
    # Docs turns "$4,000 ... $2,000" into a math equation on HTML import; find them
    for e in els:
        if "paragraph" in e:
            for el in e["paragraph"]["elements"]:
                if "equation" in el:
                    out.append([el["startIndex"], el["endIndex"]])
        if "table" in e:
            for r in e["table"]["tableRows"]:
                for c in r["tableCells"]:
                    equations(c["content"], out)
    return out
print(json.dumps({"equations": equations(tab["body"]["content"], []), "revisionId": d.get("revisionId"), "textWidth": width,
  "tables": [{"startIndex": el["startIndex"], "cols": el["table"]["columns"], "rows": el["table"]["rows"],
              "widths": [mag(c.get("width")) for c in el["table"]["tableStyle"].get("tableColumnProperties", [])]}
             for el in tab["body"]["content"] if "table" in el]}))
