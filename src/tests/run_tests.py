#!/usr/bin/env python
import sys, re, os, platform

# To avoid a clash of line endings, convert files to windows line ending
def cvt2WindowsLineEnding(inputfilename, outputfilename):
	# Check if inputfilename exists
	if os.path.exists(inputfilename):
		# Read all the files data at once
		data = open(inputfilename, "r").read()
		f = open(outputfilename, "w")
		f.write(data)
		f.close()		

def main():
	os.environ['PATH'] = ':'.join(['.', os.environ['PATH']])

	tests = ['wtest',
			 'rtest > rtest.dat && cmp rtest.dat rtestok.dat',
			 'ftest > ftest.dat && cmp ftest.dat ftestok.dat',
			 'halftest']
		 
	# There is no "cmd" command on windows so we need to use
	# the "comp" command and pipe a "N" into it to automatically 
	# stop comparing more files.
	if platform.system() == 'Windows':
		tests = ['wtest',
				'rtest > rtest.dat && echo N | comp rtest.dat rtestokwin.dat',
				'ftest > ftest.dat && echo N | comp ftest.dat ftestokwin.dat',
				'halftest']	
		cvt2WindowsLineEnding('rtestok.dat', 'rtestokwin.dat')
		cvt2WindowsLineEnding('ftestok.dat', 'ftestokwin.dat')	
	
	failed = 0
	for test in tests:
		print('Running:' + test)
		status = os.system(test)
		if status != 0:
			print('FAILED')
			failed += 1
		else:
			print('Passed')
		print

	print('Finished', len(tests), 'tests,')
	if failed == 0:
		print('All tests passed')
	else:
		print(failed, 'tests FAILED')
		exit(1)

if __name__ == '__main__':
	main()
