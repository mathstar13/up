from os import system
from random import randint
import re
from ast import literal_eval as le
pid = randint(1,999999999999999999999999999999)
d = {'atc':'','sc':0,'method':False,'global':False,'atcd':{'global':False},'ret':False,'retd':'','dir':'/home/runner/UpLang/Up'}
var = {'program':['method',''],'stdout':['method', 'SYSRUN echo $0\n'],'execpath':['var',f'sh {d["dir"]}/exec/sh'],'pid':['var',pid],'combine': ['method', 'VAR dt\nSYSRUN $execpath/combine/index $0 $1 $pid.combine.uptmp\nREAD $pid.combine.uptmp->dt\nSYSRUN $execpath/rmd $pid.combine.uptmp\nRETURN $dt\n'],'stdin': ['method', 'VAR dt\nSYSRUN $execpath/stdin/stdin $0 $pid.stdin.uptmp\nREAD $pid.stdin.uptmp->dt\nSYSRUN $execpath/rmd $pid.stdin.uptmp\nRETURN $dt\n']}
gvar = {'program':['method',''],'stdout':['method', 'SYSRUN echo $0\n'],'execpath':['var',f'sh {d["dir"]}/exec/sh'],'pid':['var',pid],'combine': ['method', 'VAR dt\nSYSRUN $execpath/combine/index $0 $1 $pid.combine.uptmp\nREAD $pid.combine.uptmp->dt\nSYSRUN $execpath/rmd $pid.combine.uptmp\nRETURN $dt\n'],'stdin': ['method', 'VAR dt\nSYSRUN $execpath/stdin/stdin $0 $pid.stdin.uptmp\nREAD $pid.stdin.uptmp->dt\nSYSRUN $execpath/rmd $pid.stdin.uptmp\nRETURN $dt\n']}
def format(txt):
	#txt = txt.replace(r'\$',r'\dollar')
	for item in sort(var).keys():
		txt = txt.replace(f'${item}',str(var[item][1]))
	#txt = txt.replace(r'\dollar','$')
	#txt = txt.replace(r'\n','\n')
	return txt
def sort(d):
	new_d = {}
	for k in sorted(d, key=len, reverse=True):
	    new_d[k] = d[k]
	return new_d
def setvar(n,ty,text,cg=True):
	var[n] = [ty,text]
	if cg:
		if d['global']:
			gvar[n] = [ty,text]
def error(n,t):
	import sys
	print(n+': '+t)
	sys.exit(1)
def parse(code):
	global var
	code = re.sub(r'//[^\n]*','',code)
	if d['atc'] == '':
		cd = code
		code = code.split(' ')
		cmd = code[0]
		ncmd = cd.replace(cmd+' ','')
		if cmd == 'START':
			d['sc'] += 1
			if code[1] in gvar:
				d['atcd']['global'] = True
			else:
				d['atcd']['global'] = False
			d['atc'] = code[1]
		elif cmd == 'WRITE':
			code = ncmd.split('->')
			var[code[1]][1] = format(code[0])
		elif cmd == 'COMMAND':
			if d['global']:
				gvar[code[1].split('=')[0]] = ['command',['',var[code[1].split('=')[1]][1],[]]]
			var[code[1].split('=')[0]] = ['command',['',var[code[1].split('=')[1]][1],[]]]
		elif cmd == 'METHOD':
			if d['global']:
				gvar[code[1]] = ['method','']
			var[code[1]] = ['method','']
		elif cmd == 'EXECUTE':
			if len(cd.split('->')) == 2:
				code[1] = code[1].split('->')[0]
			dt = var[code[1]][1]
			om = d['method']
			d['method'] = True
			oret = d['ret']
			oretd = d['retd']
			d['ret'] = False
			ov = var
			var = gvar
			cnt = 0
			for item in dt[2]:
				var[str(cnt)] = ['var',item]
				cnt += 1 
			d['global'] = False
			for line in dt[1].split('\n'):
				parse(line)
			var = ov
			d['method'] = om
			if len(cd.split('->')) == 2:
				if d['ret']:
					setvar(cd.split('->')[1],'var',d['retd'])
				else:
					setvar(cd.split('->')[1],'var','null')
			d['ret'] = oret
			d['retd'] = oretd
		elif cmd == 'SYSRUN':
			system(format(cd.replace(cmd+' ','',1)))
		elif cmd == 'RETURN':
			if d['method']:
				d['ret'] = True
				d['retd'] = format(code[1])
		elif cmd == 'READ':
			code = ncmd.split('->')
			var[code[1]][1] = open(format(code[0])).read()
		elif cmd == 'VAR':
			if d['global']:
				gvar[code[1]] = ['var','']
			var[code[1]] = ['var','']
		elif cmd == 'CLEAR':
			del var[code[1]]
		elif cmd == 'GLOBAL':
			gvar[code[1]] = var[code[1]]
		elif cmd == '':
			pass
		elif cmd == 'gvar':
			print(var)
		elif cmd == 'ADDATTRIBUTE':
			cnt = 0
			dat = ''
			for item in code:
				if cnt != 0 and cnt != 1:
					dat += ' '+item
				cnt += 1
			dt = code[1].split(',')[1]+dat
			var[code[1].split(',')[0]][1][2].append(format(dt))
		elif cmd == 'INCLUDE':
			p(open(format(code[1])).read())
		elif cmd == 'INCLUDELIB':
			p(open(d['dir']+'/lib/'+format(code[1])+'.uplib').read())
		else:
			print(f'CommandError: Unknown command "{cmd}".')
			quit()
	else:
		line = code
		if line.startswith('END'):
			d['sc'] -= 1
			if d['sc'] == 0:
				if d['atcd']['global']:
					gvar[d['atc']] = var[d['atc']]
				d['atc'] = ''
			else:
				var[d['atc']][1] += line+'\n'
		else:
			if line.startswith('START'):
				d['sc'] += 1
			var[d['atc']][1] += line+'\n'
code = open('tests/'+input('Filename: ')).read()
code += '\nCOMMAND i=program\nEXECUTE i'
def p(code):
	code = re.sub(r'\/\*[^/]*\*\/','',code)
	for line in code.split('\n'):
		parse(line)
p(code)