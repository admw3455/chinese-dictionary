# -*- coding: utf-8 -*-

import re
import io
import sys
if '3' not in sys.version.split('.')[0]:
	print('Only works with python3')
	sys.exit()

try:
	searchword=sys.argv[1]
	dictdir=str(sys.argv[-1] + 'dict.txt')
except:
	print('No search word provided, exiting')
	sys.exit(1)

if searchword == "q":
	sys.exit()

try:
	if sys.argv[2] == "freetext":
		freetext=True
	else:
		freetext=False
except:
	freetext=False

PinyinToneMark = {
    0: "aoeiuv\u00fc",
    1: "\u0101\u014d\u0113\u012b\u016b\u01d6\u01d6",
    2: "\u00e1\u00f3\u00e9\u00ed\u00fa\u01d8\u01d8",
    3: "\u01ce\u01d2\u011b\u01d0\u01d4\u01da\u01da",
    4: "\u00e0\u00f2\u00e8\u00ec\u00f9\u01dc\u01dc",
}
def decode_pinyin(s):
    s = s.lower()
    r = ""
    t = ""
    for c in s:
        if c >= 'a' and c <= 'z':
            t += c
        elif c == ':':
            assert t[-1] == 'u'
            t = t[:-1] + "\u00fc"
        else:
            if c >= '0' and c <= '5':
                tone = int(c) % 5
                if tone != 0:
                    m = re.search("[aoeiuv\u00fc]+", t)
                    if m is None:
                        t += c
                    elif len(m.group(0)) == 1:
                        t = t[:m.start(0)] + PinyinToneMark[tone][PinyinToneMark[0].index(m.group(0))] + t[m.end(0):]
                    else:
                        if 'a' in t:
                            t = t.replace("a", PinyinToneMark[tone][0])
                        elif 'o' in t:
                            t = t.replace("o", PinyinToneMark[tone][1])
                        elif 'e' in t:
                            t = t.replace("e", PinyinToneMark[tone][2])
                        elif t.endswith("ui"):
                            t = t.replace("i", PinyinToneMark[tone][3])
                        elif t.endswith("iu"):
                            t = t.replace("u", PinyinToneMark[tone][4])
                        else:
                            t += "!"
            r += t
            t = ""
    r += t
    return r

def pinyin_multiple(englishtranslation):
	plist=[]
	pinyinword2=englishtranslation.split('[')[1].split(']')[0]
	try:
		for q in pinyinword2.split(' '):
			plist.append(decode_pinyin(q))
		pword2=' '.join(plist)
	except:
		pword2=decode_pinyin(pinyinword2)
	englishtranslation=englishtranslation.replace(pinyinword2,pword2).replace('[', ' (',1).replace(']',')',1)
	return englishtranslation

with io.open(dictdir, encoding="utf-8") as dictionary:
	dictionaryfile=dictionary.readlines()

#output=io.open('output.txt', 'a', encoding="utf-8")

keywordfound=False

for i in dictionaryfile:
	if i[0] == '#':
		pass
	else:
		try:
			chineseword=(i.split('[')[0].split(' ')[1])
			plist=[]
			pinyinword=(i.split('[')[1].split(']')[0])
			try:
				for q in pinyinword.split(' '):
					plist.append(decode_pinyin(q))
				pword=' '.join(plist)
			except:
				pword=decode_pinyin(pinyinword)
			englishtranslation=(i.split('[', 1)[1].split(']', 1)[1].replace('/','',1))
			while '|' in englishtranslation:
				englishtranslation=englishtranslation.replace(str(englishtranslation.split('|',1)[0].split('/')[-1].split(' ')[-1] + '|'), '')
			while '[' in englishtranslation:
				englishtranslation=pinyin_multiple(englishtranslation)
			englishtranslation=englishtranslation[::-1]
			englishtranslation=englishtranslation.replace('/','',1)
			englishtranslation=englishtranslation[::-1]
			englishtranslation=englishtranslation.replace('/',', ')
			if freetext==True:
				if ' ' in searchword:
					searchword1=searchword.split(' ')
					freetextlist=[]
					for h in searchword1:
						if h.lower() in chineseword or h.lower() in pword or h.lower() in pinyinword or h.lower() in englishtranslation:
							if str('\t%s (%s): %s' % (chineseword, pword, englishtranslation.replace('  ', ' ').replace('\n',''))) not in freetextlist:
								freetextlist.append('\t%s (%s): %s' % (chineseword, pword, englishtranslation.replace('  ', ' ').replace('\n','')))
							else:
								pass
						else:
							try:
								freetextlist.remove('\t%s (%s): %s' % (chineseword, pword, englishtranslation.replace('  ', ' ').replace('\n','')))
							except:
								pass
							break
					if len(freetextlist) > 0:
						for k in freetextlist:
							print(k)
							keywordfound=True
				else:
					if searchword.lower() in chineseword or searchword.lower() in pword or searchword.lower() in pinyinword or searchword.lower() in englishtranslation:
						print('\t%s (%s): %s' % (chineseword, pword, englishtranslation.replace('  ', ' ').replace('\n','')))
						keywordfound=True
			else:
				if searchword == chineseword or searchword.lower() == pword or searchword.lower() == pword.replace(' ','') or searchword.lower() == pinyinword or searchword.lower() == pinyinword.replace(' ',''):
					print('\t%s (%s): %s' % (chineseword, pword, englishtranslation.replace('  ', ' ').replace('\n','')))
					keywordfound=True
				#output.write('%s (%s): %s' % (chineseword, pword, englishtranslation.replace('  ', ' ')))
		except:
			print('error')

if keywordfound is False:
	print('\tNothing found matching %s' % searchword)

#output.close()


