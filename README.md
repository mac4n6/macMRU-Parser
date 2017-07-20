# macMRU-Parser
Python script to parse the Most Recently Used (MRU) plist files on macOS into a more human friendly format.

## Usage:
`python macMRU.py [-h] [--blob_hex] [--blob_parse_human] [--blob_parse_raw] MRU_DIR`

## Output Options:
* --blob_hex - Extract the binary BLOB Bookmark data
* --blob_parse_raw - Parse the BLOB data in a raw format
* --blob_parse_human - Parse the BLOB data in a (mostly) human-friendly format


## Dependencies:      
* hexdump.py: https://pypi.python.org/pypi/hexdump    
* ccl_bplist.py: https://github.com/cclgroupltd/ccl-bplist
* mac_alias https://pypi.python.org/pypi/mac_alias

## Related Information:
https://www.mac4n6.com/blog/2016/7/10/new-script-macmru-most-recently-used-plist-parser
