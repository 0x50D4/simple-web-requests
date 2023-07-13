import argparse

parser = argparse.ArgumentParser(description="Hey I'm a desc")
parser.add_argument("filename")
parser.add_argument("-o", "--output", help="Show output")
args = parser.parse_args()

if (args.output): 
    print(str(args.output))
    
if (args.filename):
    print(args.filename)


parser.parse_args()
