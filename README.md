# Usage
This script is for use with Constellix authoritative DNS and is used for exporting all domains as BIND formatted files.  To use this script you will need your [Constellix apiKey and secretKey ](https://support.constellix.com/support/solutions/articles/47001200127-how-to-generate-an-api-key).  Once you've generated those values, look for the TODO items in the script and update with your apiKey and secretKey values.

Running the script will look something like this:

> python getBindFiles.py --per=10

The _per_ argument controls the pagination of the [list domain](https://api.dns.constellix.com/v4/docs#tag/Domains/paths/~1domains/get) API endpoint (the default is 50).  When the script is done running, a number of files will be created with the extension _.bind_.  There will be one per domain in your Constellix account.
