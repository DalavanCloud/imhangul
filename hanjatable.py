#!/usr/bin/env python

import sys, string

char_type = 'static const gunichar'
copyright = ''

def print_help():
	sys.stderr.write("Usage: hanjatable.py [Unihan database file]\n")
	sys.exit(1);

def print_description():
	desc = """/*
 * this file is generated from Unihan.txt database file by gen.py (part of
 * GTK+-2.0 input module package, imhangul)
 * You can get this database file from ftp://www.unicode.org/Public/UNIDATA/
 * or http://www.unicode.org/Public/UNIDATA/
 */
"""
 	print desc

def print_copyright():
	print '/*\n' + copyright + ' */\n'

def unicodetohexnum(str):
	return string.atoi(str[2:], 16)

def jamotosyllable(cho, jung, jong):
	syllable_base = 0xAC00
	choseong_base = 0x1100
	jungseong_base = 0x1161
	jongseong_base = 0x11A7
	njungseong = 21
	njongseong = 28

	if cho < 0x1100 and cho > 0x1112:
		return 0
	if jung < 0x1161 and jung > 0x1175:
		return 0
	if jong < 0x11A8 and jong > 0x11C2:
		return 0

	cho -= choseong_base
	jung -= jungseong_base
	jong -= jongseong_base

	ch = ((cho * njungseong) + jung) * njongseong + jong + syllable_base
	if ch >= 0xAC00 and ch <= 0xD7AF:
		return ch
	else:
		return 0

def phonetocode(phone):
	choseong_table = {
		'K':	0x1100,
		'KK':	0x1101,
		'N':	0x1102,
		'T':	0x1103,
		'TT':	0x1104,
		'L':	0x1105,
		'M':	0x1106,
		'P':	0x1107,
		'B':	0x1107,
		'PP':	0x1108,
		'S':	0x1109,
		'SS':	0x110A,
		#'':	0x110B,
		'C':	0x110C,
		'CC':	0x110D,
		'CH':	0x110E,
		'KH':	0x110F,
		'TH':	0x1110,
		'PH':	0x1111,
		'H':	0x1112
	}
	jungseong_table = {
		'A':	0x1161,
		'AY':	0x1162,
		'YA':	0x1163,
		'YAY':	0x1164,
		'E':	0x1165,
		'EY':	0x1166,
		'YE':	0x1167,
		'YEY':	0x1168,
		'O':	0x1169,
		'WA':	0x116A,
		'WAY':	0x116B,
		'OY':	0x116C,
		'WOY':	0x116C,
		'YO':	0x116D,
		'WU':	0x116E,
		'WE':	0x116F,
		'WEY':	0x1170,
		'WI':	0x1171,
		'YU':	0x1172,
		'U':	0x1173,
		'UY':	0x1174,
		'I':	0x1175
	}
	jongseong_table = {
		'K':	0x11A8,
		'KK':	0x11A9,
		'KS':	0x11AA,
		'N':	0x11AB,
		'NC':	0x11AC,
		'NH':	0x11AD,
		'T':	0x11AE,
		'L':	0x11AF,
		'LK':	0x11B0,
		'LM':	0x11B1,
		'LP':	0x11B2,
		'LS':	0x11B3,
		'LTH':	0x11B4,
		'LPH':	0x11B5,
		'LH':	0x11B6,
		'M':	0x11B7,
		'P':	0x11B8,
		'PS':	0x11B9,
		'S':	0x11BA,
		'SS':	0x11BB,
		'NG':	0x11BC,
		'C':	0x11BD,
		'CH':	0x11BE,
		'KH':	0x11BF,
		'TH':	0x11C0,
		'PH':	0x11C1,
		'H':	0x11C2
	}
	if choseong_table.has_key(phone[:2]):
		choseong = choseong_table[phone[:2]]
		phone = phone[2:]
	elif choseong_table.has_key(phone[:1]):
		choseong = choseong_table[phone[:1]]
		phone = phone[1:]
	else:
		choseong = 0x110B
	
	if jungseong_table.has_key(phone[:3]):
		jungseong = jungseong_table[phone[:3]]
		phone = phone[3:]
	elif jungseong_table.has_key(phone[:2]):
		jungseong = jungseong_table[phone[:2]]
		phone = phone[2:]
	elif jungseong_table.has_key(phone[:1]):
		jungseong = jungseong_table[phone[:1]]
		phone = phone[1:]
	else:
		sys.stderr.write("%s: phonetic data error\n" % phone)
		return 0

	if jongseong_table.has_key(phone[:3]):
		jongseong = jongseong_table[phone[:3]]
		phone = phone[3:]
	elif jongseong_table.has_key(phone[:2]):
		jongseong = jongseong_table[phone[:2]]
		phone = phone[2:]
	elif jongseong_table.has_key(phone[:1]):
		jongseong = jongseong_table[phone[:1]]
		phone = phone[1:]
	else:
		jongseong = 0x11A7

	# print "%x + %x + %x" % ( choseong, jungseong, jongseong )
	hangulcode = jamotosyllable(choseong, jungseong, jongseong)

	return hangulcode;


# start main procedure
data_file_name = "Unihan.txt"

if len(sys.argv) == 2:
	data_file_name = sys.argv[1]

try:
	data_file = open(data_file_name, 'r')

except:
	sys.stderr("Cant open file: %s\n" % data_file_name)
	help()
	sys.exit(1)

gather_copyright = 0
table = { }
for line in data_file.readlines():
	# check for comment, jump over comments
	if line[0] == '#':
		if gather_copyright == 0:
			if string.find(line, "Format information:") != -1 :
				gather_copyright = 1
				continue
			copyright += ' * ' + string.strip(line[1:]) + '\n'
			continue
		else:
			continue
		
	# check for korean phonetic data
	if string.find(line, "kKorean") < 0:
		continue

	tokens = string.split(line)
	hanjacode = unicodetohexnum(tokens[0])
	for hangulphone in tokens[2:]:
		hangulcode = phonetocode(hangulphone)
		if hangulcode == 0:
			continue

		if table.has_key(hangulcode):
			table[hangulcode].append(hanjacode)
		else:
			table[hangulcode] = [ hanjacode ]

data_file.close()

print_description()
print_copyright()

list = table.keys()
list.sort()

for key in list:
	print char_type + " hangul_%X[] = {" % key
	print "\t0x%X," % key

	i = 0
	table[key].sort()
	for hanja in table[key]:
		if i == 0:
			print "\t",
		sys.stdout.write("0x%X," % hanja)
		i = i + 1
		if i == 10:
			i = 0
			sys.stdout.write("\n")

	if i == 0:
		print "\t0"
	else:
		print "\n\t0"
	print "};"


print char_type + " *hanja_table[] = {"
i = 0
for key in list[:-1]:
	if i == 0:
		print "\t",
	sys.stdout.write("hangul_%X, " % key)
	i = i + 1
	if i == 5:
		i = 0
		sys.stdout.write("\n")

if i == 0:
	print "\t",
sys.stdout.write("hangul_%X" % list[-1])
i = i + 1
if i == 5:
	i = 0
	sys.stdout.write("\n")

if i == 0:
	print "};"
else:
	print "\n};"


