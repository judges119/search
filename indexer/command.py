import sys
import scrape

a = getattr(scrape, sys.argv[1])
a(sys.argv[2])