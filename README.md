# ansible_inventory_parser
Parse ansible inventory files/directories to ssh config

# install requirements
```bash
pip install -r ./requirements.txt
```

# docopt

Usage:
  parse.py [--header=<FILE>] [--output=<FILE>] [--verbose] [--indent=<INDENT>] INVENTORY...  
  parse.py -h | --help  
  parse.py -V | --version  

Options:
  -h --help                 Show this screen.  
  -V --version              Show version.  
  -v --verbose              Debug.  
  -o=FILE --output=<FILE>   Save output as file.  
  -H=FILE --header=<FILE>   Load custom header. [default: header]  
  -i --indent=<SPACE>       Indent. [default: 2]  

# example
```bash
./parse.py /etc/ansible/hosts -o /tmp/config -H header.example
```
