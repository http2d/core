#!/usr/bin/env python

"""huffman-gen.py: Generates huffman tables for HPAC encoding and decoding based on the draft document.

It uses a template, default is huffman_tables.tpl, to render the final
output.

We can choose our source between those already known to the script:
	- EC_HTML: Editor's copy in HTML
	- EC_XML: Editor's copy in XML
	- EC_TXT: Editor's copy in TXT
	- WGD_HTML: Less recent, more official Working Group Draft
Or specify our own source file.

It tries not to modify the output file, huffman_tables.c by default, if
possible. That way it will not trigger a recompile of the source code.

Tries to do as little work as possible, so if it detects that the source
file hasn't changed (etag, date, size) from the last time it will
consider the output file to be up to date and stop there. Won't even
bother downloading the source file.

If you change sources it will not be able to tell that way if the file
has been updated.

If he doesn't think they are the same it will generate the arrays and
compare them with the current contents of the output file. If the arrays
are the same he doesn't touch the output file.

Only when they don't match he will write the output file.
Script can be forced to always generate output file.

To be able to tell if the file has been updated we have added a line in
huffman_tables.c file (second line).

"""

__author__ = "Gorka Eguileor"
__version__ = "1.0.0"
__maintainer__ = "Gorka Eguileor"
__email__ = "gorka@eguileor.com"
__status__ = "Development"


# IMPORT SECTION

import sys
import argparse
import re
import os

if sys.version_info[0] == 2:
    import urllib2
else:
    import urllib.request as urllib2
    import functools
    reduce = functools.reduce


# CONSTANTS SECTION

HUFFMAN_TABLES_TEMPLATE = "huffman_tables.tpl"
OUTPUT_FILE = "huffman_tables.c"

DEFAULT_EC_XML_SOURCE = "https://raw.github.com/http2/http2-spec/master/draft-ietf-httpbis-header-compression.xml"
DEFAULT_EC_HTML_SOURCE = "http://http2.github.io/http2-spec/compression.html"
DEFAULT_EC_TXT_SOURCE = "http://http2.github.com/http2-spec/compression.txt"
DEFAULT_WGD_HTML_SOURCE = "http://tools.ietf.org/html/draft-ietf-httpbis-header-compression"

SOURCES = {"EC_HTML":DEFAULT_EC_HTML_SOURCE,
           "EC_XML":DEFAULT_EC_XML_SOURCE,
           "EC_TXT":DEFAULT_EC_TXT_SOURCE,
           "WGD_HTML":DEFAULT_WGD_HTML_SOURCE}

ID_TPL_VERSION_CONTROL = r"/*{TPL_VERSION_CONTROL}*/"
ID_TPL_HPACK_HUFFMAN_SIZE = r"/*{TPL_HPACK_HUFFMAN_SIZE}*/"
ID_TPL_HPACK_HUFFMAN = r"/*{TPL_HPACK_HUFFMAN}*/"
ID_TPL_DECODE_TABLE = r"/*{TPL_DECODE_TABLE}*/"

TPL_WARNING_MESSAGE = "THIS FILE IS AUTOGENERATED, DO NOT TOUCH! MODIFY TEMPLATE AND GENERATOR IF NEEDED"


# CLASSES SECTION

class BruteParser():

	"""Brute force parser for the Huffman Table
	Instead of having multiple parsers, one for XML files, one for HTML files and one for TXT files we use a brute force aproach.
	Using regular expressions we extract the relevant section and then remove anything in between data lines (page footers and headers).

	Functions:
		__init__
		close -- After we feed the data we should close the parser
		feed -- Feeds the data to the parser which stores the result in the data attribute

	Attribute:
		data -- Contains parsed data
	"""

	def __init__(self):
		self.data = []

	def close(self):
		return

	def feed(self, data):
		"""Feed data to the parser.

		Keyword arguments:
			data -- Text which contains somewhere the huffman table

		If successful the result will be available in the data attribute which is a list of dictionaries with the following entries:
			'symb' -- Symbol represented in the dictionary
			'symb_N' -- Numeric value of the symbol (number)
			'bit_len' -- Length in bits of the huffman code (number)
			'MSB_bits' -- List of 0 and 1 that represent the huffman code. MSB first
			'LSB_hex' -- Huffman code in hex representation. LSB first
		"""

		# We force the retrieval to have 257 entries, otherwise the huffman table is not complete
		r = re.search("(?P<data>(\s*?.+?\s*\(\s*\d+\s*\)\s*[01\|]+\s*(\[\s*(?P<opt_bit_len>\d+)\s*\]\s*)?[\da-fA-F]+\s*\[\s*(?P<bit_len>(?(opt_bit_len)(?P=opt_bit_len)|\d+))\s*\](.|\n)*?){257,257})",data,re.MULTILINE)

		# We'll use another regex to retrieve only the lines with data and to split its contents.
		re_data = re.compile("\s*?((?P<symb>(\'.+?\'|[^.\s]+?))|\s)\s*?\(\s*(?P<symb_N>\d+?)\)\s*?(?P<MSB_bits>[01\|]+)\s*?(\[(?P<opt_bit_len>\d+)\]\s*?)?(?P<LSB_hex>[\da-f]+?)\s*?\[\s*(?P<bit_len>(?(opt_bit_len)(?P=opt_bit_len)|\d+))\s*\]")

		if r:
			# Split lines for processing
			lines = r.group('data').splitlines()

			# Generate the list by cleaning the data: converting to numbers, removing the '|' from MSB_bits and changing it to a list
			self.data = [{'symb': d.group('symb'),
			              'symb_N': int(d.group('symb_N')),
			              'bit_len': int(d.group('bit_len')),
			              'MSB_bits': [int(ch) for ch in d.group('MSB_bits').replace("|","")],
			              'LSB_hex': d.group('LSB_hex')
			             } for d in map(re_data.search, lines) if d]
		return


class bTree():

	"""Binary Tree specific for huffman codes
	This is not a generic BTree class, so most generic functions are non existant and we only have specific functions needed.
	It uses class atributes to work, so only 1 tree can be used at a time.

	Functions:
		__init__ -- Inits a node or a root node
		buildFromLeaf -- Builds the nodes needed for decoding a specific symbol and sets the leaf Id
		is_leaf -- Tells you if the node is a leaf of the decoding tree
		is_root -- Tells you if the node is the root of the decoding tree
		traverse -- Traverses the tree using given path and returns decoded symbols along the way
		getNodes -- Returns a list of all the nodes of the tree
		assignIds -- Assigns Id to the nodes of the tree leaving the leafs alone

	Attributes:
		node_id -- For leafs this is the symbol decoded by the path from the root, for nodes it's their reference if assigned
		children -- List with 2 bTree children 0 and 1
	"""

	_root = None
	verbos = 0

	def __init__(self, node_id=None, setRoot=False, verbos=0):
		"""Init the tree or node if you don't assign ids remember to call assignIds later on"""

		self.node_id = node_id
		self.children = [None,None]
		self.verbos = verbos
		if setRoot:
			self.__class__._root = self

		verbosity(self.verbos, 3, "Creating node " + str(node_id) + " [root=" + str(self.is_root()) + "]")

	def buildFromLeaf(self, path, leaf_id):
		"""Builds the nodes needed for the decoding path and creates the leaf with leaf_id.
		It doesn't give Ids to intermediate nodes, so you must call assigIds later on.
		You can assign the ids after every leaf or after creating the whole tree.

		Arguments:
			path -- List of 0 and 1
			leaf_id -- Id to asign to the leaf
		"""

		verbosity(self.verbos, 3, "Building leaf " + str(leaf_id) + " with path " + str(path))

		pos = self
		for p in path:
			if not pos.children[p]:
				verbosity(self.verbos, 3, "Node for " + str(p) + " doesn't exist")
				pos.children[p] = bTree()

			verbosity(self.verbos, 3, "Moving to " + str(p))
			pos = pos.children[p]

		verbosity(self.verbos, 3, "Setting leaf id to " + str(leaf_id))
		pos.node_id = leaf_id		

	def is_leaf(self):
		return not (self.children[0] or self.children[1])

	def is_root(self):
		return self._root == self

	def traverse(self, path):
		"""Traverse the tree using the given path and when a leaf is reached go back to the root and continue.

		Argument:
			path -- List of 0 and 1
		
		Returns a tuple with:
			The end node
			List of decoded symbols (leafs_ids)
			List of the node ids it has visited while traversing that path. Including the end node
		"""

		nodes = []
		decoded = []

		pos = self
		verbosity(self.verbos, 3, "Traversing " + str(path) + " from " + str(pos.node_id))

		if pos.is_leaf():
			verbosity(self.verbos, 3, "We began at a leaf, going to root")
			pos = self._root

		for p in path:
			nodes.append(pos.node_id)

			# If we can go the way we want
			if pos.children[p]:
				verbosity(self.verbos, 3, "Going " + str(p) + " from " + str(pos.node_id) + " we get to " + str(pos.children[p].node_id))
				pos = pos.children[p]
				if pos.is_leaf():
					verbosity(self.verbos, 3, "Leaf reached, decoded " + str(pos.node_id) + " and going back to root")
					decoded.append(pos.node_id)
					nodes.append(pos.node_id)
					pos = self._root

			# If we cannot go the way we want
			else:
				verbosity(self.verbos, 0, red("Tried to traverse to " + str(p) + " from " + str(pos.node_id) + " but that path doesn't exist"))
				raise Exception("Cannot traverse that path")

		nodes.append(pos.node_id)
		if pos.is_leaf():
			verbosity(self.verbos, 3, "Finished at leaf, decoded " + str(pos.node_id))
			decoded.append(pos.node_id)
		else:
			verbosity(self.verbos, 3, "Finished at node " + str(pos.node_id))

		verbosity(self.verbos, 3, "We walked throught these nodes " + str(nodes))
		return (pos,decoded,nodes)

	def getNodes(self, includeLeafs=False):
		"""Returns a list of all the nodes of the tree, leafs can be included too"""

		pending = [self]
		while pending:
			pos = pending.pop()
			if pos:
				if pos.is_leaf() and not includeLeafs:
					continue
				yield pos
				pending += [pos.children[1],pos.children[0]]

	def assignIds(self):
		"""Assigns Id to the nodes of the tree in order leaving the leafs alone"""
		node_id = 0
		pending = [self]

		verbosity(self.verbos, 3, "Assigning IDs to tree")
		while pending:
			pos = pending.pop()

			if pos:
				if not pos.is_leaf():
					pos.node_id = node_id
					node_id += 1
					pending += [pos.children[1],pos.children[0]]


# FUNCTIONS SECTION


def getFlags(node, decod):
	"""Returns the flags accept and decoded sysmbol for a given node with a given decoding"""
	x = 0
	if node.is_root():
		x |= 1
	if len(decod):
		x |= 2
	return x


def getFirst(decod):
	"""Returns the firs decoded symbol or 0 if we haven't decoded anything"""
	if decod:
		return decod[0]
	return 0


def gen_decode_table(data, verbos=0, bCheckTree=True):
	"""Generates the decode_table contents array and returns it as a string"""

	# Check in the data that there is no encoding with less than 4 bits, if it exists, we have a problem
	# because the hpack_huffman_decode in huffman.c won't work since we can get 2 bytes decoded from 4 bits
	# but the code and tables only allow 1 byte decode per 4 bits.
	verbosity(verbos, 3, "Checking that we have no problem with the bit length of the symbols")
	e = filter(lambda x: x['bit_len'] < 4, data)
	if list(e):
		raise Exception("Problem with min bits")

	# Now we reconstruct the huffman binary tree
	verbosity(verbos, 2, "Reconstructing huffman binary tree")
	decodeTree = bTree(0, True, verbos)
	for d in data:		
		decodeTree.buildFromLeaf(d['MSB_bits'],d['symb_N'])

	# And assign the Ids to intermediate nodes
	decodeTree.assignIds()

	# Stream padding can have from 0 to 7 bits and they come from the EOS encoding,
	# so we need to get the first 7 nodes to that encoding because when we finish
	# decoding in those nodes we've had a proper finish
	node,decod,eos_padding = decodeTree.traverse(data[-1]['MSB_bits'][:7])

	# Remove first entry (root node)
	eos_padding = eos_padding[1:]

	# Check that the tree is right
	if bCheckTree:
		verbosity(verbos, 3, "Checking that the tree we built is right")
		# We go 1 by 1 checking that they are properly decoded
		for d in data:
			node,decod,nodes = decodeTree.traverse(d['MSB_bits'])
			bError = (1 != len(decod)) or not node.is_root()
			if not bError:
				bError = decod[0] != d['symb_N']
			if bError:
				verbosity(verbos, 0, red("ERROR: path " + str(d['MSB_bits']) + " results in " + str(decod) + " instead of " + str(d['symb_N'])))

		# Now we try to decode all symbols together as a stream
		a = map(lambda x: ([x['symb_N']],x['MSB_bits']), data)
		b = reduce(lambda x,y: (x[0]+y[0],x[1]+y[1]),a)

		node,decod,nodes = decodeTree.traverse(b[1])
		if b[0] != decod or not node.is_root():
			verbosity(verbos, 0, red("Error in traverse\nsymb_N=" + str(b['symb_N']) + "\ndecod=" + str(decod) + "\nnode=" + str(node.node_id)))

	# For each nodes we need to know where do we go with each 4 bit path
	# So we create a list of all the possible combinations of arrays of 0 and 1 for 4 bits
	verbosity(verbos, 2, "Generating all routes from each node")
	combinations = [[(x&8)>>3,(x&4)>>2,(x&2)>>1,x&1] for x in range(0,16)]

	# And a list of tuples with the origin node and all possible traverse for those 16 paths
	all_traverse = [(n,[n.traverse(p) for p in combinations]) for n in decodeTree.getNodes()]		

	verbosity(verbos, 2, "Rendering array")
	result = ""
	for n,t in all_traverse:
		# Comment at the beginning of the line that represents the symbol number
		s = "    /* {:>3} */ ".format(n.node_id)+"{"

		for x in t:
			# We are never supposed to get to a full EOS decoding,
			# so if we reach it it means there's been an error
			if 256 == getFirst(x[1]):
				nid = -1
				decod = '0'
				flags = '0'
			else:
				nid = x[0].node_id
				decod = str(getFirst(x[1]))
				flags = getFlags(x[0],x[1])

				# For those cases where we could be decoding the padding we consider them as accepted (proper end of stream)
				if x[0].node_id in eos_padding:
					flags |= 1
			
			s += "{" + str(nid) + ",0x" + str(flags) + "," + decod + "},"
		result += s + "},\n"

	# Remove the last comma and new line
	return result[:-1]


def get_args():
	"""Takes care of the arguments to the script"""

	desc = 'Parse HPACK spec to generate Huffman tables for ' + OUTPUT_FILE + ' using template file ' + HUFFMAN_TABLES_TEMPLATE + ' .\nFiles may be stores in\n\t- Filesystem\n\t- Http\n\t- Https'
	epil = 'Examples:\n\t' + sys.argv[0] + ' -i ./draft.html --vv -f\n\t' + sys.argv[0] + ' -s WGD_HTML'
	parser = argparse.ArgumentParser(description=desc,epilog=epil,formatter_class=argparse.RawTextHelpFormatter)

	group = parser.add_mutually_exclusive_group()
	group.add_argument('-i','--input', help='Input source, can be a file or URL.\nDefault is to use the source of the current draft:\n  ' + DEFAULT_EC_XML_SOURCE,required=False,default=None)
	group.add_argument('-s','--source', help="Input source default is EC_XML.\nOptions:\n\t- EC_HTML: Editor's copy in HTML\n\t- EC_XML: Editor's copy in XML\n\t- EC_TXT: Editor's copy in TXT\n\t- WGD_HTML: Less recent, more official Working Group Draft",required=False, choices=SOURCES.keys(), default="EC_XML")

	parser.add_argument('-o','--output',help='Output file name. Default value is ' + OUTPUT_FILE, required=False, default=OUTPUT_FILE)
	parser.add_argument('-t','--template', help='Template file to use. Default is ' + HUFFMAN_TABLES_TEMPLATE,required=False,default=HUFFMAN_TABLES_TEMPLATE)
	parser.add_argument('-f','--force',help="Force generation of output file even when it's up to date", required=False, default=False, action="store_true")
	parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="count", default=0)

	args = parser.parse_args()

	# urllib2 doesn't handle files without protocol specifier, so we add file:// and the path if we're given a relative path
	if args.input:
		if not re.match("\w+://",args.input):
			args.input = "file://" + os.path.realpath(args.input)
	# If we are not given an input file we use the default for the type of source
	else:
		args.input = SOURCES[args.source]

	# We have to add the path to our output and template files
	dirname,filename = os.path.split(os.path.realpath(__file__))
	args.output = os.path.join(dirname, args.output)
	args.template = os.path.join(dirname, args.template)

	if args.verbosity >= 2:
		print ("Using parameters:")
		for arg in vars(args).items():
			print ("\t" + arg[0] + "=" + str(arg[1]))
		print ()
	return args


ESC   = chr(27) + '['
RESET = '%s0m' % (ESC)


def green (s):
	"""Turn string green. Useful for verbosity"""
	return ESC + '0;32m' + s + RESET


def red (s):
	"""Turn string red. Useful for verbosity"""
	return ESC + '0;31m' + s + RESET

def dark_red (s):
	"""Turn string dark red. Useful for verbosity"""
	return ESC + '1;31m' + s + RESET


def verbosity(verb, min_lvl, text):
	"""Prints debugging info depending on the verbosity level"""
	if min_lvl <= verb:
		print (text)


def get_current_data(cfg):
	"""Reads the output file to see what are the contents of the arrays and the version control string
	Returns a dictionary with:
		'etag' -- Etag of the source file used to render the file. As stored in the version control string
		'date' -- Date of the source file used to render the file. As stored in the version control string
		'size' -- Size of the source file used to render the file. As stored in the version control string
		'hpack_huffman' -- Contents of the hpack_huffman array
		'decode_table' -- Contents of the decode_table array
	"""

	vc = None
	hh = None
	dc = None

	try:
		verbosity(cfg.verbosity, 2, "Checking contents of file " + cfg.output)
		with open(cfg.output, 'r') as f:
			template = f.read()

		verbosity(cfg.verbosity, 2, "File read, proceed to parse it")

		# We get the version control string
		vc = re.search("/\*\s*\((?P<warning>\s*\".*?\")\s*,\s*(?P<date>.+?)\s*,\s*(?P<size>\d+?)\s*,\s*(?P<etag>\".*?\")\s*\)\s*\*/", template, re.MULTILINE)

		# We get the hpack_huffman array contents (only the part that we generate)
		hh = re.search("\n(?P<hpack_huffman>(\s*\{\s*\d+\s*,\s*0x\w+?\s*}\s*,?\s*\n?)+)\n", template, re.MULTILINE)

		# We get the decode_table array contents (only the part that we generate)
		dc = re.search("\n(?P<decode_table>(\s*/\*\s*\d+\s*\*/\s*\{(\s*\{\s*.*?\s*\}\s*,?)+\s*\},?)+)", template, re.MULTILINE)

	except IOError:
		verbosity(cfg.verbosity, 2, "File " + cfg.output + "doesn't exist")

	if vc and hh and dc:
		verbosity(cfg.verbosity, 2, "File parsed correctly")
		verbosity(cfg.verbosity, 2, "Contents are: \n\tDate: " + vc.group('date') + "\n\tSize: " +
		          vc.group('size') + "\n\tetag: " + vc.group('etag'))
		verbosity(cfg.verbosity, 3, "\thpack_huffman:\n" + hh.group('hpack_huffman') + "\n\tdecode_table:\n" + dc.group('decode_table'))

		return {'etag':vc.group('etag'),
		        'date':vc.group('date'),
		        'size':vc.group('size'),
		        'hpack_huffman':hh.group('hpack_huffman'),
		        'decode_table':dc.group('decode_table')}

	verbosity(cfg.verbosity, 2 ,"Couldn't parse contents, considered as if not up to date")

	return {'etag':None,
	        'date':None,
	        'size':None,
	        'hpack_huffman':None,
	        'decode_table':None}


def get_data(cfg):
	"""Gets the Huffman codes table from the source, the current contents of the output file, the new version control string and tells you if the file is up to date
	The function tries to do the least work possible.
	If  etag or date and file size are the same on the output and the source it will not retrieve the source and consider it "up to date", unless we used -f parameter.
	When it's not "up to date" the contents of the output file will be retrieved and the source will be parsed.

	Function returns a dictionary with entries:
		'up_to_date'
	        'data' -- Data used by gen_hpack_huffman and gen_decode_table functions
	        'version_control' -- Version control string that will be writen to output file if we finally write it
	        'current_data' -- Contents of the output file
	"""

	data = None
	rev = None
	version_control = None

	verbosity(cfg.verbosity, 1, "Checking source")
	verbosity(cfg.verbosity, 2, "Reading from " + cfg.input)
	try:
		sock = urllib2.urlopen(cfg.input)
		verbosity(cfg.verbosity, 2, "Input file available")

	except (urllib2.HTTPError, urllib2.URLError) as e:
		verbosity(cfg.verbosity, 0, red("Error while trying to get " + cfg.input + "\n\t" + str(e)))
		return

	headers = sock.info()

	# Get data from file or url: etag, date and size
	source_size = headers['Content-Length']
	if 'ETag' in headers.keys():
		etag = headers['ETag']
	else:
		etag = "\"\""

	if 'last-modified' in headers.keys():
		source_date = headers['last-modified']
	else:
		source_date = headers['Date']

	verbosity(cfg.verbosity, 2, "Source has " + source_size + " bytes and was last modified on " + source_date + " [etag=" + etag + "]")

	# Get current data from the output file
	current_data = get_current_data(cfg)

	up_to_date = current_data and ((etag and (etag != '""') and (etag == current_data['etag'])) or ((source_date == current_data['date']) and (source_size == current_data['size'])))

	if cfg.force or not up_to_date:
		if 'Content-Type' in headers.keys() and '=' in headers['Content-Type']:
			content_type = headers['Content-Type'].split('=')[-1]
		else:
			content_type = 'utf-8'

		_tmlSource = sock.read().decode(content_type)

		verbosity(cfg.verbosity, 1, "Parsing source file")
		verbosity(cfg.verbosity, 3, "Contents of source file are:\n" + _tmlSource)

		parser = BruteParser()
		parser.feed(_tmlSource)
		parser.close()
		data = parser.data

		verbosity(cfg.verbosity, 3, "Parsed data:\n" + str(data))

		version_control = '/*("' + TPL_WARNING_MESSAGE + '",' + source_date + "," + source_size + "," + etag + ")*/" 
		verbosity(cfg.verbosity, 2, "Source file version control: " + version_control)

	sock.close()

	return {'up_to_date':up_to_date,
	        'data':data,
	        'version_control':version_control,
	        'current_data':current_data}


def gen_hpack_huffman(data):
	"""Generates the hpack_huffman array and returns a tuple with the length of the array and the content of the array both as strings"""

	content = ""
	for d in data:
		content += "    { " + str(d['bit_len']) + ", 0x" + d['LSB_hex'] + "u },\n"
	# We remove the last comma and new line
	return (str(len(data)), content[:-2])


def render_output(cfg, version_control, hpack_huffman, decode_table):
	"""Renders the output file using the template and the data needed

	Arguments:
		cfg -- Config that has verbosity level, template file name and output file name
		version_control -- String with the info on the file used to render the output
		hpack_huffman -- As returned by gen_hpack_huffman function
		decode_table -- As returned by gen_decode_table function
	"""

	try:
		verbosity(cfg.verbosity, 2, "Reading template")
		with open(cfg.template, 'r') as f:
			huffman_tables_s = f.read()

	except IOError:
		verbosity(cfg.verbosity, 0, red("Could not open template file"))
		return False

	verbosity(cfg.verbosity, 2, "Rendering output file")
	huffman_tables_s = huffman_tables_s.replace(ID_TPL_VERSION_CONTROL, version_control)
	huffman_tables_s = huffman_tables_s.replace(ID_TPL_HPACK_HUFFMAN_SIZE, hpack_huffman[0])
	huffman_tables_s = huffman_tables_s.replace(ID_TPL_HPACK_HUFFMAN, hpack_huffman[1])
	huffman_tables_s = huffman_tables_s.replace(ID_TPL_DECODE_TABLE, decode_table)

	verbosity(cfg.verbosity, 2, "Writing file " + cfg.output)
	try:
		with open(cfg.output,"w") as f:
			f.write(huffman_tables_s)
	except IOError as e:
		verbosity(cfg.verbosity, 0, red("Error writing file " + cfg.output + "\n" + str(e)))
		return False

	return True


def main():
	args=get_args()

	verbosity(args.verbosity, 0, dark_red("Auto generating Huffman tables"))
	data = get_data(args)

	if not data:
		return

	if data['up_to_date'] and not args.force:
		verbosity(args.verbosity, 0, green("File " + args.output + " is up to date. Nothing to do."))
		return

	if not data['data']:
		verbosity(args.verbosity, 0, red("No data could be parsed from input file."))
		return

	verbosity(args.verbosity, 1, "Generating hpack_huffman array")
	hpack_huffman = gen_hpack_huffman(data['data'])

	verbosity(args.verbosity, 1, "Generating decode_table array")
	decode_table = gen_decode_table(data['data'], args.verbosity)

	if hpack_huffman[1] == data['current_data']['hpack_huffman'] and decode_table == data['current_data']['decode_table'] and not args.force:
		verbosity(args.verbosity, 0, green("File " + args.output + " has same contents as source. Nothing to do."))
		return

	verbosity(args.verbosity, 1, "Rendering output")
	result = render_output(args,data['version_control'],hpack_huffman,decode_table)
	if result:
		verbosity(args.verbosity, 0, green("Finished rendering  " + args.output + " file"))


if __name__ == '__main__':
	main()

