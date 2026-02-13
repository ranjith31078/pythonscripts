from dateutil.parser import parse
import sys

# Measure Boomi process using the log

def get_measured_lines(filename):
	measurements = []
	prev_date = None
	prev_line = None

	with open(filename) as log_file:
		for line in log_file:
			words = line.split()
			cur_date = parse(words[0])
			if prev_date is not None:
				measurements.append(((cur_date - prev_date).total_seconds(), \
					prev_line, '', ' '.join(words[2:])))
			prev_date = cur_date
			prev_line = ' '.join(words[2:])
			

	return measurements

def print_lines(lines):
	for line in lines:
		if (int(line[0]) > 2): # 2 secs
			print ("%10d %s\n%10s %s\n%s" % (line + (''.ljust(150, '-'),)))

def start(filename):
	lines = get_measured_lines(filename)
	lines.sort(reverse=True)
	print_lines(lines)

if __name__ == '__main__':
	start(sys.argv[1] if len(sys.argv) > 1 else "c:\\temp\\process.log")